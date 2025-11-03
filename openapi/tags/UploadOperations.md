# Upload Operations

> **Optional Functionality**: Upload operations are optional DRS extensions. Clients should check `/service-info` for upload support before attempting to use these endpoints.

Upload functionality allows clients to negotiate with servers on mutually convenient storage technologies and then register uploads as DRS objects through a three-phase workflow:

1. **Request Upload URLs**: POST `/uploadrequest` with file metadata to receive upload methods and credentials
2. **Upload Files**: Use returned URLs and credentials to upload files to storage using existing upload mechanisms. DRS is not involved in this step at all, DRS simply allows the client and server to agree on a mutually convenient storage service.
3. **Register Objects**: POST `/objects/register` to register associated DRS objects with the server, so they are available to DRS clients

This approach separates storage service and credential negotiation from file transfer and object registration, supporting a vendor-neutral means of sharing data in a DRS network. The `/objects/register` endpoint can also be used independently to register existing data without the upload workflow.

**Bulk-Only Design**: Upload operations only support bulk requests to simplify implementation and reflect real-world usage patterns. Bioinformatics workflows typically involve uploading multiple related files together (e.g., BAM + BAI, VCF + TBI, or analysis result sets), making bulk operations a natural fit. Single files are handled as lists with one element.

## Service Discovery

Check `/service-info` for upload capabilities:

```json
{
  "drs": {
    "uploadSupported": true,
    "supportedUploadMethods": ["s3", "https", "gs"],
    "maxUploadSize": 5368709120,
    "maxUploadRequestLength": 50,
    "validateUploadChecksums": true,
    "validateUploadFileSizes": false,
    "relatedFileStorageSupported": true
  }
}
```

Key fields:
- `uploadSupported`: Upload operations available
- `supportedUploadMethods`: Available storage backends  
- `maxUploadSize`: File size limit (bytes)
- `maxUploadRequestLength`: Files per request limit
- `validateUploadChecksums`/`validateUploadFileSizes`: Server validation behavior
- `relatedFileStorageSupported`: Files from same upload request stored under common prefixes

## Upload Methods

Supported storage backends:
- **https**: Presigned POST URLs for HTTP uploads
- **s3**: Direct S3 upload with temporary AWS credentials
- **gs**: Google Cloud Storage with OAuth2 tokens
- **ftp/sftp**: Traditional file transfer protocols using negotiated credentials

Servers may return a subset of advertised methods based on file characteristics, for example they may choose to store large objects such as WGS BAM files in different backends to small csv files.

## Related File Storage (Optional)

Servers MAY store files from the same upload request under common prefixes, enabling bioinformatics workflows that expect co-located files:

- **CRAM + CRAI**: Alignment files with index files (samtools, IGV)
- **VCF + TBI**: Variant files with tabix indexes  
- **FASTQ.ora + ORADATA.tar.gz**: Compressed files with associated reference data

Check `relatedFileStorageSupported` in service-info or examine upload URLs for common prefixes.

## Object Registration

After upload, register files as DRS objects using POST `/objects/register`:

**Atomic Transactions**: Registration is all-or-nothing. If ANY candidate fails, the ENTIRE request fails and no objects are registered.

**Requirements**:
- Complete metadata (name, size, checksums, MIME type)
- Access methods pointing to file locations  
- Valid authorization (if required)
- Do not include server-generated fields (id, self_uri, timestamps)

Server mints unique IDs and returns complete DRS objects.

**Standalone Usage**: The `/objects/register` endpoint can be used independently to register existing data that is already stored in accessible locations, without using the `/uploadrequest` workflow. This is useful for registering pre-existing datasets or files uploaded through other means.

## Authentication & Validation

**Authentication**: Supports GA4GH Passports, Basic auth, and Bearer tokens.

**Checksums**: Required for all files (SHA-256, MD5, or IANA-registered algorithms). Servers MAY validate checksums and file sizes as advertised in service-info flags.



## Error Handling

**Client Errors (4xx)**: Invalid metadata (400), missing auth (401), insufficient permissions (403)
**Server Errors (5xx)**: Storage unavailable (500), capacity limits (503)
**Upload-Specific**: Checksum/size validation failures, quota exceeded, timeouts

## Best Practices

**Clients**: Check service-info first, calculate checksums, implement retry logic
**Servers**: Use short-lived credentials, support multiple upload methods, implement rate limiting
**Security**: Time-limited credentials, single-use URLs, proper logging

## Security Considerations

**Credential Scoping**: Implementers SHOULD scope upload credentials to the minimum necessary permissions and duration. Credentials should:
- Allow write access only to the specific upload URL/path provided
- Have the shortest practical expiration time (typically 15 minutes to 1 hour)
- Be restricted to the specific file size and content type when possible
- Not grant broader storage access beyond the intended upload location

This principle of least privilege reduces security exposure if credentials are compromised or misused.

## Example Workflows

### Simple HTTPS Upload

**1. Request Upload Method**
```http
POST /uploadrequest
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

**Response:**
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

**2. Upload via HTTPS**
```bash
# Simple PUT upload to presigned URL
curl -X PUT "https://uploads.example.org/presigned-upload?signature=FAKE_SIG" \
  --data-binary @variants.vcf
```

**3. Register DRS Object**
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

**Response:**
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
          "access_id": "https",
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

**1. Request Upload Methods for Related Files**
```http
POST /uploadrequest
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

**Response:**
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

**2. Upload Both Files to S3**
```bash
# Upload BAM and index files using the supplied credentials (note common prefix)
aws s3 cp sample.bam s3://genomics-uploads/x7k9m/sample.bam
aws s3 cp sample.bam.bai s3://genomics-uploads/x7k9m/sample.bam.bai
```

**3. Register Both DRS Objects**
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

**Response:**
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