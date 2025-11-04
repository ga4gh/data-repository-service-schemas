# Upload Operations

> **Optional Functionality**: Upload operations are **optional** extensions to the DRS API. Not all DRS servers are required to implement upload functionality. Clients should check for the availability of upload endpoints before attempting to use them.

The DRS API provides optional upload functionality that allows clients to obtain upload methods and temporary credentials for storing files before they are registered as DRS objects. This capability extends the traditional read-only nature of DRS to support data ingestion workflows.

The upload feature is designed as a **negotiation mechanism** between client and server to identify mutually convenient storage services and access patterns. The DRS specification defines the negotiation protocol and credential exchange, but the details of how data is physically uploaded to the underlying storage systems are outside the scope of the DRS specification and depend on the specific storage service protocols (S3, HTTPS, etc.). DRS does not reinvent existing storage protocols, but rather facilitates their discovery and authorization.

## Overview

Upload operations in DRS follow a three-phase approach:

1. **Upload Request Phase**: Clients request upload methods by providing file metadata
2. **File Upload Phase**: Clients use the returned upload methods to store files in the underlying storage system
3. **DRS Object Registration Phase**: Clients register the uploaded files as DRS objects using the POST `/objects` endpoint

This design separates the concerns of obtaining upload credentials from the actual file transfer and subsequent DRS object registration, providing flexibility in how files are uploaded while maintaining security through temporary, scoped credentials.

## Server Implementation Requirements

Upload operations are **entirely optional**. Servers implement uploads when they support data ingestion, collaborative workflows, or staging areas. Read-only servers, mirrors, or security-constrained environments typically do not implement uploads.

## Client Discovery and Compatibility

Clients should implement proper discovery mechanisms to determine upload support:

### Service Info Discovery (Recommended)

The most reliable way to discover upload support is through the `/service-info` endpoint:

```json
{
  "drs": {
    "uploadSupported": true,
    "supportedUploadMethods": ["s3", "https", "gs"],
    "maxUploadSize": 5368709120,
    "maxUploadRequestLength": 50,
    "validateUploadChecksums": true,
    "validateUploadFileSizes": false
  }
}
```

**Service Info Fields:**
- **`uploadSupported`**: Boolean indicating if upload operations are available
- **`supportedUploadMethods`**: Array of upload method types the server supports
- **`maxUploadSize`**: Maximum file size in bytes (optional)
- **`maxUploadRequestLength`**: Maximum files per upload request (optional)
- **`validateUploadChecksums`**: Boolean indicating if server validates uploaded file checksums (optional, defaults to false)
- **`validateUploadFileSizes`**: Boolean indicating if server validates uploaded file sizes (optional, defaults to false)

### Client Best Practices

1. **Always check `/service-info` first** for `uploadSupported`, `supportedUploadMethods`, and validation flags
2. **Respect server limits** (`maxUploadSize`, `maxUploadRequestLength`)
3. **Handle missing upload support gracefully** with alternative workflows
4. **Prepare for validation behavior** based on `validateUploadChecksums`/`validateUploadFileSizes` flags

## Upload Request Endpoint

The `/uploadrequest` endpoint accepts POST requests containing file metadata and returns available upload methods with temporary credentials.

### Request Structure

Upload requests must include:
- **File metadata**: Name, size, MIME type, and checksums for each file
- **Authentication**: Optional GA4GH Passport tokens for authorization
- **File descriptions**: Optional human-readable descriptions and aliases

**Note**: Servers do not validate the provided MIME type against the actual file content. Clients are responsible for providing accurate MIME type information.

**Upload Method Selection**: Clients must select one or more upload methods from the server response to upload their files. The selected upload methods determine the storage locations, and clients must include corresponding access methods in the DRS object registration that point to these same storage locations.

### Response Structure

Upload responses provide:
- **DRS object metadata**: Pre-assigned IDs and URIs for the files
- **Upload methods**: Available storage protocols (S3, HTTPS, GCS, etc.)
- **Temporary credentials**: Time-limited access tokens or keys
- **Upload URLs**: Specific endpoints for file transfer

## Supported Upload Methods

- **https**: Presigned POST URLs for simple HTTP uploads
- **s3**: Direct S3 upload with temporary AWS credentials (supports multipart uploads)
- **gs**: Google Cloud Storage upload with OAuth2 tokens
- **ftp/sftp**: Traditional file transfer protocols
- **globus**: High-performance transfer service for large files

**Note**: While servers advertise their supported upload methods in `service-info`, the actual upload response may include only a subset of these methods. Servers may choose specific upload methods based on file characteristics such as size, type, or internal policies.

## Authentication

Upload operations support GA4GH Passports (embedded in request body), Basic authentication, and Bearer tokens for flexible authorization.

## File Integrity and Validation

All upload requests must include checksums to ensure data integrity:

### Required Checksums
- At least one checksum per file is mandatory for client requests
- Supported algorithms include SHA-256, MD5, and IANA-registered hash types
- Multiple checksums per file are supported for enhanced verification

### Server Validation Options
Servers MAY validate checksums and/or file sizes (advertised via `validateUploadChecksums`/`validateUploadFileSizes` flags) but are not required to do so. Validation increases security but adds computational overhead.

### Validation Process
1. Client calculates checksums before requesting upload methods
2. **Server MAY validate checksums and file sizes** during or after upload, but is not required to do so
3. If server performs validation and detects mismatches, it SHOULD reject the upload or registration
4. Servers that do not perform validation rely on client-provided metadata for DRS object registration
5. Successful upload (with or without server validation) enables DRS object registration

## Integration with DRS Object Lifecycle

Upload operations are designed to integrate seamlessly with the broader DRS object lifecycle:

### Pre-Upload Phase
1. Client prepares files and calculates metadata
2. Client requests upload methods via `/uploadrequest`
3. Server responds with upload options and pre-assigned DRS identifiers

### Upload Phase
1. Client selects one or more appropriate upload methods from the server response
2. Client uploads files using the selected methods' credentials and URLs
3. Storage system receives and stores files at the locations corresponding to the selected upload methods

### Post-Upload Phase
1. Files are available in storage with pre-assigned DRS identifiers
2. **DRS Object Registration**: Clients use the POST `/objects` endpoint to register uploaded files as DRS objects
3. DRS objects can be queried using standard DRS endpoints
4. Access methods are automatically configured based on storage location

## DRS Object Registration

After successfully uploading files using the `/uploadrequest` endpoint, clients must register the uploaded files as DRS objects to make them accessible through the DRS API. This can be accomplished using either:

- **Single Object Registration**: POST `/objects/{object_id}` for registering one object at a time
- **Bulk Object Registration**: POST `/objects` for registering multiple objects at once

### Registration Process

1. **Prepare DRS Object Metadata**: Create fully formed DRS object structures with:
   - The object ID returned from the upload request
   - Complete metadata (name, size, checksums, MIME type, timestamps)
   - Access methods that correspond to the upload methods used during file upload
   - Optional descriptions and aliases

2. **Choose Registration Method**:
   - **Single Object**: POST to `/objects/{object_id}` with `object` field containing one DRS object
   - **Bulk Objects**: POST to `/objects` with `objects` array containing multiple DRS objects

3. **Submit Registration Request**: Include GA4GH Passport tokens for authorization (if required)

4. **Confirm Registration**: Server validates and registers the DRS objects, making them available for subsequent queries

### Single Object Registration

The POST `/objects/{object_id}` endpoint operates in two modes:

- **Register Mode**: When the request body contains an `object` field with a fully formed DRS object, the endpoint registers the provided object
- **Retrieve Mode**: When the `object` field is missing, the endpoint behaves as a GET request with passport authentication

### Bulk Object Registration

The POST `/objects` endpoint operates in two modes:

- **Register Mode**: When the request body contains an `objects` array with fully formed DRS objects, the endpoint registers the provided objects
- **Retrieve Mode**: When the request body contains `bulk_object_ids` array, the endpoint behaves as a bulk retrieval operation returning metadata for the specified objects

### Registration Requirements

For successful DRS object registration after upload:

- **Complete Metadata**: All required DRS object fields must be present and valid
- **Valid Access Methods**: Access methods must point to the actual uploaded file locations
- **Checksum Consistency**: Checksums in registration request SHOULD match those provided during upload request
- **Authorization**: Appropriate GA4GH Passport tokens must be provided if required by the server
- **Bulk Efficiency**: Multiple objects can be registered in a single request for better performance

**Note**: Servers MAY verify that registered object metadata matches uploaded file characteristics, but are not required to do so.

### Example Registration Workflows

**Single Object Registration:**
```
1. Upload file via /uploadrequest
   → Receive object ID: "drs_obj_123"

2. File is uploaded to storage location
   → File available at provided upload URL

3. Register DRS object via POST /objects/drs_obj_123
   → Request body contains object field with fully formed DRS object
   → Server validates and registers the object

4. Query registered object via GET /objects/drs_obj_123
   → Standard DRS object retrieval now works
```

**Bulk Object Registration:**
```
1. Upload files via /uploadrequest
   → Receive object IDs: "drs_obj_123", "drs_obj_456"

2. Files are uploaded to storage locations
   → Files available at provided upload URLs

3. Register DRS objects via POST /objects
   → Request body contains objects array with fully formed DRS objects
   → Server validates and registers all objects in bulk

4. Query registered objects via GET /objects/drs_obj_123
   → Standard DRS object retrieval now works for all registered objects
```

## Error Handling

Upload operations include comprehensive error handling:

### Client Errors (4xx)
- **400 Bad Request**: Invalid file metadata or malformed requests
- **401 Unauthorized**: Missing or invalid authentication credentials
- **403 Forbidden**: Insufficient permissions for upload operations

### Server Errors (5xx)
- **500 Internal Server Error**: Storage system unavailable or configuration issues
- **503 Service Unavailable**: Temporary capacity limitations or maintenance

### Upload-Specific Errors
- **Checksum validation failures** (only if server performs validation)
- **File size mismatches** (only if server performs validation)
- File size limit exceeded (server-imposed limits)
- Storage quota exceeded
- Upload timeout or connection failures

## Best Practices

**Clients**: Calculate checksums, handle multiple upload methods, implement retry logic, check service-info for validation behavior.

**Servers**: Use short-lived credentials, provide multiple upload methods when possible, implement consistent validation (if any), use rate limiting.

**Security**: Time-limited credentials, single-use URLs, proper logging, input validation.

## Example Workflows

### Simple File Upload
1. **Check service info** via GET `/service-info` to confirm upload support and available methods
2. Calculate SHA-256 checksum of local file
3. Send upload request with file metadata to `/uploadrequest`
4. Receive HTTPS upload URL, headers, and pre-assigned DRS object ID
5. POST file to upload URL using multipart form data
6. Verify upload success
7. **Register DRS object** via POST `/objects/{object_id}` with fully formed DRS object metadata
8. Confirm DRS object is accessible via standard DRS endpoints

### Large File Upload with S3
1. **Check service info** to confirm S3 upload support and size limits
2. Prepare large genomic dataset file
3. Request upload methods specifying file size via `/uploadrequest`
4. Receive S3 upload method with temporary AWS credentials and pre-assigned DRS object ID
5. Use AWS SDK to perform multipart upload
6. Monitor upload progress and handle retries
7. Confirm upload completion
8. **Register DRS object** via POST `/objects/{object_id}` with complete metadata and S3 access methods
9. Verify DRS object availability through standard DRS queries

### Authenticated Upload with Passports
1. **Check service info** to confirm upload support and understand available methods
2. Obtain GA4GH Passport tokens for dataset access
3. Include passports in upload request body to `/uploadrequest`
4. Server validates passport visas and permissions
5. Receive authorized upload methods and pre-assigned DRS object IDs
6. Upload files to authorized storage locations
7. **Register DRS objects** via POST `/objects` with the same passport tokens (bulk registration)
8. Server validates passports again during registration
9. DRS objects become available with appropriate access controls based on passport authorization

### Bulk Upload and Registration
1. **Check service info** to confirm upload support and bulk limits
2. Request upload methods for multiple files via `/uploadrequest`
3. Receive upload methods and pre-assigned DRS object IDs for all files
4. Upload all files using their respective upload methods
5. **Register all DRS objects** via POST `/objects` with `objects` array containing all uploaded files
6. All objects become available simultaneously through standard DRS endpoints