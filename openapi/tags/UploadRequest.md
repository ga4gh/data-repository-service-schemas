# Upload Requests and Object Registration

> **Optional Functionality**: Upload and object registration are optional DRS extensions. Clients should check `/service-info` for `uploadRequestSupported` and `objectRegistrationSupported` before attempting to use these endpoints.

The DRS upload and object registration endpoints allows clients to negotiate with servers on mutually convenient storage backends and then register uploads as DRS objects through a three-phase workflow:

1. **Request Upload URLs**: POST `/upload-request` with file metadata to receive upload methods and credentials
2. **Upload Files**: Use returned URLs and credentials to upload files to storage using existing upload mechanisms. DRS is not involved in this step at all, DRS simply enables clients and servers to agree on a mutually convenient storage service.
3. **Register Objects**: POST `/objects/register` to register "candidate" DRS objects with the server

This approach separates storage service and credential negotiation from file transfer and object registration, supporting a vendor-neutral means of sharing data in a DRS network.

The `/objects/register` endpoint can be used independently to register existing data without using the `/upload-request` endpoint, and servers can choose to only support object registration and not file uploads by setting the `uploadRequestSupported` and `objectRegistrationSupported` flags appropriately in `/service-info`.

Upload requests and object registration endpoints only support bulk requests to simplify implementation and reflect real-world usage patterns. Bioinformatics workflows often involve uploading multiple related files together (e.g., BAM and VCF files with their indices, or analysis result sets), making bulk operations a natural fit. Single files/objects are handled as lists with one element. Implementations of the `/objects/register` endpoint SHOULD implement transaction semantics so that either all of the objects are successfully registered or none of them are, and clients should be robust to this behaviour. Transaction semantics for the `/upload-request` are encouraged but not required due to the variety and complexity of data transfer technologies.

The `/upload-request` endpoint does not require any state to be maintained on the DRS server (intermediate DRS object IDs etc.) it is simply a means for a server to provide details of where a client can upload data, and it should ensure that it trusts the client before providing such details. This means that if uploads fail and there is no later call to `/objects/register` there is no DRS state to manage, simplifying server implementation.

Servers SHOULD ensure that any data from unsuccessful uploads (e.g. incomplete multi-part uploads) are cleaned up, for example by using lifecycle configuration in the backend storage. There is _no_ means of requiring that a client ultimately registers a DRS object pointing at data uploaded, and so servers should consider implementing some form of storage "garbage" collection (or simply set a short lifecycle policy on the upload location and move uploaded data that is later registered as DRS objects to other locations, updating the `access_method`s accordingly). Servers should also implement some means of constraining upload size (quotas etc.) to protect against accidental or malicious unconstrained uploads.

The `/upload-request` endpoint can return one or more `upload_method`s of different types for each requested file, and backend specific details such as bucket names, object keys and credentials are supplied in a generic `upload_details` field. A straightforward implementation might return an single time-limited pre-signed POST URL as the `post_url` for an `upload_method` of type `https` which incorporates authentication into the URL, but because DRS is often used for large files such as BAMs and CRAMs we also want to support more sophisticated upload approaches implemented by storage backends such as multi-part uploads, automatic retries etc. The `upload_details` field can also be used to include bucket names, keys and temporary credentials that can be used in native clients and SDKs. This offers a natural way to adapt this protocol to new storage technologies. Refer to the examples below for some suggested implementations.

## Service Discovery

Check `/service-info` for upload capabilities:

```json
{
  "drs": {
    "uploadRequestSupported": true,
    "objectRegistrationSupported": true,
    "supportedUploadMethods": ["s3", "https", "gs"],
    "maxUploadSize": 5368709120,
    "maxUploadRequestLength": 50,
    "maxRegisterRequestLength": 50,
    "validateUploadChecksums": true,
    "validateUploadFileSizes": false,
    "relatedFileStorageSupported": true
  }
}
```

Upload related fields:

- `uploadRequestSupported`: Upload request operations available via `/upload-request`
- `objectRegistrationSupported`: Object registration operations available via `/objects/register`
- `supportedUploadMethods`: Available storage backends  
- `maxUploadSize`: File size limit (bytes)
- `maxUploadRequestLength`: Files per request limit for upload requests
- `maxRegisterRequestLength`: Candidate objects per request limit for registration
- `validateUploadChecksums`/`validateUploadFileSizes`: Server validation behavior
- `relatedFileStorageSupported`: Files from same upload request stored under common prefixes

## Upload Methods

Upon receipt of a request for an upload method for a specific file, the server will respond with one or more `upload_method` with associated `type` and corresponding `upload_details` with upload locations, temporary credentials etc. These details are specific to backend implementations.

Example storage backends:

- **https**: Presigned POST URLs for HTTP uploads
- **s3**: Direct S3 upload with temporary AWS credentials
- **gs**: Google Cloud Storage with OAuth2 tokens
- **ftp/sftp**: Traditional file transfer protocols using negotiated credentials

Servers may return a subset of advertised methods based on file characteristics, for example they may choose to store large objects such as WGS BAM files in different backends to small csv files.

## Related File Storage (Optional)

Servers MAY support storing files from the same upload request under common prefixes, enabling bioinformatics workflows that expect co-located files:

- **CRAM + CRAI**: Alignment files with index files
- **VCF + TBI**: Variant files with tabix indexes  
- **FASTQ.ora + ORADATA.tar.gz**: Compressed files with associated reference data

Check `relatedFileStorageSupported` in service-info or examine upload URLs for common prefixes.

## Object Registration

After upload, clients can register files in bulk as DRS objects using POST `/objects/register`. Registration is all-or-nothing. If any candidate object fails to be registered in the server, the entire request fails and no objects are registered.

**Candidate DRS object equirements**:

- Complete metadata (name, size, checksums, MIME type)
- Access methods pointing to file locations  
- Valid authorization (if required)
- Do not include server-generated fields (id, self_uri, timestamps)

Upon receipt of candidate objects for registration the server will create unique object IDs and returns complete DRS objects. Note that the server is not obliged to retain the clients supplied `access_method`s and is free to move data to different locations/backends once the object is registered. This means that a server can choose to receive uploads in a dedicated "dropzone", with hard quotas and additional security, and then move them to more permanent storage once the DRS object is registered. Clients SHOULD NOT cache the response from `/objects/register` as the `access_method`s might change after registration.

The `/objects/register` endpoint can also be used independently to register existing data that is already stored in accessible locations, without using the `/upload-request` workflow. This is useful for registering pre-existing datasets or files uploaded through other means. Servers may choose only to support registration and not uploads, and should advertise this in `/service-info`

## Authentication & Validation

**Authentication**: Supports GA4GH Passports, Basic auth, and Bearer tokens.

**Checksums**: Required for all files (SHA-256, MD5, or IANA-registered algorithms). Servers MAY validate checksums and file sizes as advertised in service-info flags.

## Error Handling

**Client Errors (4xx)**:

- Invalid metadata (400)
- Missing auth (401)
- Insufficient permissions (403)

**Server Errors (5xx)**:

- Storage unavailable (500)
- Capacity limits (503)

## Best Practices

**Clients**: Check service-info first, calculate checksums, be robust to failed object registration
**Servers**: Use short-lived tightly scoped credentials, support multiple upload methods, implement rate limiting, ensure unique storage backend names to avoid inadvertent overwrites (e.g. using UUIDs), ensure that quotas are enforced and incomplete or unregistered uploads are deleted
**Security**: Time-limited credentials, single-use URLs, logging for audit

## Security Considerations

**Credential Scoping**: Implementers SHOULD scope upload credentials to the minimum necessary permissions and duration. Credentials should:

- Allow write access only to the specific upload URL/path provided
- Have the shortest practical expiration time (e.g. 15 minutes to 1 hour)
- Be restricted to the specific file size and content type when possible
- Not grant broader storage access beyond the intended upload location

This principle of least privilege reduces security exposure if credentials are compromised or misused.

## Example Workflows

### Simple HTTPS Upload

Upload Request:

```http
POST /upload-request
Content-Type: application/json

{
  "requests": [
    {
      "name": "variants.vcf",
      "size": 52428800,
      "mime_type": "text/plain",
      "checksums": [
        {
          "checksum": "5d41402abc4b2a76b9719d911017c592",
          "type": "md5"
        }
      ]
    }
  ]
}
```

Response:

```json
{
  "responses": [
    {
      "name": "variants.vcf",
      "size": 52428800,
      "mime_type": "text/plain",
      "checksums": [
        {
          "checksum": "5d41402abc4b2a76b9719d911017c592",
          "type": "md5"
        }
      ],
      "upload_methods": [
        {
          "type": "https",
          "access_url": {
            "url": "https://uploads.example.org/variants.vcf"
          },
          "upload_details": {
            "post_url": "https://uploads.example.org/presigned-upload?signature=FAKE_SIG"
          }
        }
      ]
    }
  ]
}
```

Upload via HTTPS:

```bash
# Simple PUT upload to presigned URL
curl -X PUT "https://uploads.example.org/presigned-upload?signature=FAKE_SIG" \
  --data-binary @variants.vcf
```

Register DRS Object:

```http
POST /objects/register
Content-Type: application/json

{
  "candidates": [
    {
      "name": "variants.vcf",
      "size": 52428800,
      "mime_type": "text/plain",
      "checksums": [
        {
          "checksum": "5d41402abc4b2a76b9719d911017c592",
          "type": "md5"
        }
      ],
      "access_methods": [
        {
          "type": "https",
          "access_url": {
            "url": "https://uploads.example.org/variants.vcf"
          }
        }
      ],
      "description": "Variant calls in VCF format"
    }
  ]
}
```

Response:

```json
{
  "objects": [
    {
      "id": "drs_obj_f6e5d4c3b2a1",
      "self_uri": "drs://drs.example.org/drs_obj_f6e5d4c3b2a1",
      "name": "variants.vcf",
      "size": 52428800,
      "mime_type": "text/plain",
      "created_time": "2024-01-15T10:45:00Z",
      "updated_time": "2024-01-15T10:45:00Z",
      "version": "1.0",
      "checksums": [
        {
          "checksum": "5d41402abc4b2a76b9719d911017c592",
          "type": "md5"
        }
      ],
      "access_methods": [
        {
          "type": "https",
          "access_url": {
            "url": "https://uploads.example.org/variants.vcf"
          }
        }
      ],
      "description": "Variant calls in VCF format"
    }
  ]
}
```

### S3 Bulk Upload (BAM + Index)

Request Upload Methods for Related Files

```http
POST /upload-request
Content-Type: application/json

{
  "requests": [
    {
      "name": "sample.bam",
      "size": 1073741824,
      "mime_type": "application/octet-stream",
      "checksums": [
        {
          "checksum": "d41d8cd98f00b204e9800998ecf8427e",
          "type": "md5"
        }
      ]
    },
    {
      "name": "sample.bam.bai",
      "size": 2097152,
      "mime_type": "application/octet-stream",
      "checksums": [
        {
          "checksum": "098f6bcd4621d373cade4e832627b4f6",
          "type": "md5"
        }
      ]
    }
  ]
}
```

Response:

```json
{
  "responses": [
    {
      "name": "sample.bam",
      "size": 1073741824,
      "mime_type": "application/octet-stream",
      "checksums": [
        {
          "checksum": "d41d8cd98f00b204e9800998ecf8427e",
          "type": "md5"
        }
      ],
      "upload_methods": [
        {
          "type": "s3",
          "access_url": {
            "url": "s3://genomics-uploads/x7k9m/sample.bam"
          },
          "upload_details": {
            "bucket": "genomics-uploads",
            "key": "x7k9m/sample.bam",
            "access_key_id": "FAKE_ACCESS_KEY_123",
            "secret_access_key": "FAKE_SECRET_KEY_456",
            "session_token": "FAKE_SESSION_TOKEN_789",
            "expires_at": "2024-01-15T12:00:00Z"
          }
        }
      ]
    },
    {
      "name": "sample.bam.bai",
      "size": 2097152,
      "mime_type": "application/octet-stream",
      "checksums": [
        {
          "checksum": "098f6bcd4621d373cade4e832627b4f6",
          "type": "md5"
        }
      ],
      "upload_methods": [
        {
          "type": "s3",
          "access_url": {
            "url": "s3://genomics-uploads/x7k9m/sample.bam.bai"
          },
          "upload_details": {
            "bucket": "genomics-uploads",
            "key": "x7k9m/sample.bam.bai",
            "access_key_id": "FAKE_ACCESS_KEY_123",
            "secret_access_key": "FAKE_SECRET_KEY_456",
            "session_token": "FAKE_SESSION_TOKEN_789",
            "expires_at": "2024-01-15T12:00:00Z"
          }
        }
      ]
    }
  ]
}
```

Upload Both Files to S3:

```bash
# Upload BAM and index files using the supplied credentials (note common prefix)
aws s3 cp sample.bam s3://genomics-uploads/x7k9m/sample.bam
aws s3 cp sample.bam.bai s3://genomics-uploads/x7k9m/sample.bam.bai
```

Register Both DRS Objects:

```http
POST /objects/register
Content-Type: application/json

{
  "candidates": [
    {
      "name": "sample.bam",
      "size": 1073741824,
      "mime_type": "application/octet-stream",
      "checksums": [
        {
          "checksum": "d41d8cd98f00b204e9800998ecf8427e",
          "type": "md5"
        }
      ],
      "access_methods": [
        {
          "type": "s3",
          "access_id": "s3",
          "access_url": {
            "url": "s3://genomics-uploads/x7k9m/sample.bam"
          }
        }
      ],
      "description": "BAM alignment file"
    },
    {
      "name": "sample.bam.bai",
      "size": 2097152,
      "mime_type": "application/octet-stream",
      "checksums": [
        {
          "checksum": "098f6bcd4621d373cade4e832627b4f6",
          "type": "md5"
        }
      ],
      "access_methods": [
        {
          "type": "s3",
          "access_id": "s3",
          "access_url": {
            "url": "s3://genomics-uploads/x7k9m/sample.bam.bai"
          }
        }
      ],
      "description": "BAM index file"
    }
  ]
}
```

Response:

```json
{
  "objects": [
    {
      "id": "drs_obj_a1b2c3d4e5f6",
      "self_uri": "drs://drs.example.org/drs_obj_a1b2c3d4e5f6",
      "name": "sample.bam",
      "size": 1073741824,
      "mime_type": "application/octet-stream",
      "created_time": "2024-01-15T10:30:00Z",
      "updated_time": "2024-01-15T10:30:00Z",
      "version": "1.0",
      "checksums": [
        {
          "checksum": "d41d8cd98f00b204e9800998ecf8427e",
          "type": "md5"
        }
      ],
      "access_methods": [
        {
          "type": "s3",
          "access_id": "s3",
          "access_url": {
            "url": "s3://genomics-uploads/x7k9m/sample.bam"
          }
        }
      ],
      "description": "BAM alignment file"
    },
    {
      "id": "drs_obj_b2c3d4e5f6a1",
      "self_uri": "drs://drs.example.org/drs_obj_b2c3d4e5f6a1",
      "name": "sample.bam.bai",
      "size": 2097152,
      "mime_type": "application/octet-stream",
      "created_time": "2024-01-15T10:30:00Z",
      "updated_time": "2024-01-15T10:30:00Z",
      "version": "1.0",
      "checksums": [
        {
          "checksum": "098f6bcd4621d373cade4e832627b4f6",
          "type": "md5"
        }
      ],
      "access_methods": [
        {
          "type": "s3",
          "access_id": "s3",
          "access_url": {
            "url": "s3://genomics-uploads/x7k9m/sample.bam.bai"
          }
        }
      ],
      "description": "BAM index file"
    }
  ]
}
```
