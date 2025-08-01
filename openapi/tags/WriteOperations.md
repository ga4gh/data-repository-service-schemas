# DRS Write Operations

DRS 1.6 introduces optional write operations that allow clients to create, update, and delete DRS objects. These operations are designed to work with cloud storage systems through a two-phase upload process.

## Write Capability Discovery

Servers advertise write support through the `service-info` endpoint in the `drs.writeCapabilities` section:

- `supported`: Whether write operations are available
- `storage_locations`: Available storage backends (S3, GCS, Azure, etc.)
- `max_object_size`: Maximum file size limit
- `supported_checksums`: Checksum algorithms for validation

## Authorization Model

Write operations require authentication and use a permission-based authorization model:

- `GET /write/authorizations` returns storage locations accessible to the authenticated user
- Each location specifies available permissions: `create`, `update`, `delete`
- Quota information helps clients understand storage limits

## Two-Phase Upload Process

### Phase 1: Initialize Object
- `POST /objects` creates a DRS object in `pending` state
- Server returns presigned upload URL for the specified storage location
- Object metadata is stored but content is not yet available

### Phase 2: Upload and Finalize  
- Client uploads data directly to cloud storage using provided URL
- `POST /objects/{id}/finalize` marks upload complete with checksum verification
- Object transitions to `available` state with populated access methods

## Multi-Location Support

Objects can be uploaded to multiple storage locations for redundancy:

- `POST /objects/{id}/upload-urls` requests additional upload URLs
- Each location upload is tracked independently  
- Finalize operation reports all successfully uploaded locations

## Object States

- `pending`: Object created, awaiting upload
- `uploading`: Upload in progress (optional state)
- `available`: Upload complete and verified
- `failed`: Upload or validation failed
- `deleted`: Object has been removed

## Update Operations

- Metadata-only updates (name, description) don't change object state
- Content updates (size, checksums) trigger new upload process
- `PUT /objects/{id}` returns upload URLs if content change detected

## Error Handling

- `400 Bad Request`: Malformed request data
- `409 Conflict`: Object state conflicts (e.g., already exists)
- `422 Unprocessable Entity`: Checksum validation failures
- `413 Request Too Large`: Exceeds server size limits

## Best Practices

- Always check write authorizations before creating objects
- Verify checksums locally before finalizing uploads
- Handle upload URL expiration gracefully
- Use appropriate storage locations based on access patterns
- Monitor quota usage to avoid hitting limits