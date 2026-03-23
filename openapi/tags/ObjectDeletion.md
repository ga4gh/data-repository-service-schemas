# Object Deletion

> **Optional Functionality**: Delete support is an **optional** extension to the DRS API. Not all DRS servers are required to implement delete functionality. Clients should check for the availability of delete endpoints before attempting to use them.

DRS delete functionality allows suitably authenticated clients to request that DRS objects are removed from the server and, optionally, to request that the server attempt to delete the underlying data.

Servers should ensure that they trust clients from whom they receive delete requests. The `delete_object_metadata` parameter allows clients to request that the server preserves the object metadata record after deletion (soft delete) rather than permanently removing it. Servers that support this mode advertise `metadataRetentionSupported` in service-info. Soft-deleted objects return 410 Gone on read and access requests. Because delete support is optional, servers operating in untrusted environments may choose not to support delete operations at all.

In combination with the `/objects/register` endpoint, metadata only delete requests offer a means for clients to update DRS metadata without affecting the underlying data, and without introducing additional update operations which would complicate server implementation.

Clients can express a preference that the underlying data referred to by the deleted DRS object(s) is deleted with the `delete_storage_data` parameter. Servers are free to interpret this as they choose, and can advertise whether they support it at all with the `deleteStorageDataSupported` flag. Servers that choose to attempt to honour the request need not perform this operation synchronously and may, for example, register the file for later deletion or implement soft deletion with versioning etc. Implementations may also choose to ensure that no other DRS object registered in the server refers to the underlying data before deleting. Servers may not have the necessary permissions to delete the data from the backend even if they would like to do so, or may encounter errors when they attempt deletion. In the case that a DRS object refers to data stored in multiple backends (e.g. has multiple `access_methods`) the server may attempt to delete the data from all or only some of the backends.

For these reasons clients MUST NOT depend on the server deleting the underlying storage data even if the server advertises that `deleteStorageDataSupported` and the client sets the `delete_storage_data` flag.

In situations where the DRS server controls the storage backend, DRS delete support offers a convenient vendor-neutral way for clients to update and delete DRS objects and corresponding data.

For bulk deletes using the `/objects/delete` endpoint the server SHOULD implement transaction semantics: if any object fails validation or deletion, the entire request should fail and no objects are deleted and no attempt is made to delete from underlying storage for any object.

## Design principles

- **Optional**: Delete support is completely optional
- **Safety**: Preserves underlying data in storage unless explicitly requested
- **Backward compatible**: No impact on existing DRS functionality
- **Flexible authentication**: Supports GA4GH Passports, Bearer tokens, API keys
- **Use PUT rather than DELETE**: GA4GH Passports require request bodies, which DELETE methods don't reliably support across all HTTP infrastructure. PUT ensures broad compatibility.

## Service Discovery

Check `/service-info` for delete capabilities:

```json
{
  "drs": {
    "uploadRequestSupported": true,
    "objectRegistrationSupported": true,
    "supportedUploadMethodTypes": ["s3", "https"],
    "relatedFileStorageSupported": true,
    "deleteSupported": true,
    "maxBulkDeleteLength": 100,
    "deleteStorageDataSupported": true,
    "metadataRetentionSupported": true
  }
}
```

- **`deleteSupported`**: Whether server supports deletion
- **`maxBulkDeleteLength`**: Maximum objects per bulk delete request
- **`deleteStorageDataSupported`**: Whether server can attempt to delete underlying storage files
- **`metadataRetentionSupported`**: Whether server supports preserving metadata after deletion (soft delete via `delete_object_metadata: false`)

### Single Object Delete: `PUT /objects/{object_id}/delete`

```bash
curl -X PUT "https://drs.example.org/objects/drs_object_123456/delete" \
  -H "Content-Type: application/json" \
  -d '{"delete_object_metadata": true, "delete_storage_data": false}'
# Response: 204 No Content (indicates metadata deletion success only)
```

**Note**: HTTP responses indicate metadata deletion status only. Storage deletion (`delete_storage_data: true`) is a best effort attempt with no guarantee of success.

### Bulk Object Delete: `PUT /objects/delete`

```bash
curl -X PUT "https://drs.example.org/objects/delete" \
  -H "Content-Type: application/json" \
  -d '{
    "bulk_object_ids": ["obj_1", "obj_2", "obj_3"],
    "delete_object_metadata": true,
    "delete_storage_data": false
  }'
# Response: 204 No Content (all deleted) or 4xx error (none deleted, transactional)
```

## Authentication

**GA4GH Passports** (in request body):

```json
{"passports": ["eyJhbGci..."], "delete_storage_data": false}
```

**Bearer Tokens** (in headers):

```bash
curl -H "Authorization: Bearer token" -d '{"delete_storage_data": false}' ...
```

## Delete Parameters

The delete endpoints accept two independent parameters that control what is deleted:

### `delete_object_metadata` (default: `false`)

Controls whether the DRS object metadata record is permanently removed or preserved.

**`delete_object_metadata: false`** (default): The server marks the object as deleted but preserves the metadata record (soft delete). Read and access endpoints return 410 Gone with a standard Error response body for the object. This requires `metadataRetentionSupported: true` in service-info; servers that do not support metadata retention silently ignore this parameter and permanently delete metadata.

**`delete_object_metadata: true`**: Permanently removes the metadata record. The object ID will no longer resolve and cannot be recovered.

### `delete_storage_data` (default: `false`)

Controls whether the server attempts to delete underlying storage files.

**`delete_storage_data: false`** (default): Underlying storage files are preserved.

**`delete_storage_data: true`**: Requests the server attempt to delete underlying storage files (requires `deleteStorageDataSupported: true`). **Success is not guaranteed** -- deletion may fail due to permissions, network issues, or storage service errors. Clients should not depend on storage deletion success.

## Update Pattern

Rather than introducing additional operations and endpoints for updating DRS objects, servers can allow clients to use the metadata-only deletion and object registration endpoints to create a new DRS object with updated metadata while leaving the underlying data in place. Note that DRS only supports updating the `access_methods` and adding additional checksums to existing objects while maintaining the same DRS object ID. Any other changes to an object will require deletion and re-registration.

**Metadata update steps:**

1. Delete metadata: `PUT /objects/{id}/delete` with `delete_object_metadata: true`
2. Re-register object: `POST /objects/register` with updated metadata

```bash
# Delete metadata permanently (preserves storage)
curl -X PUT ".../objects/obj_123/delete" -d '{"delete_object_metadata": true}'
# Re-register with updates
curl -X POST ".../objects/register" -d '{"candidates": [{"name": "updated.txt", ...}]}'
```

## Error Responses

- **400**: Unsupported storage deletion or invalid request parameters
- **403**: Insufficient permissions for any object in the request
- **404**: Any object not found or delete endpoints not supported by server
- **413**: Bulk request exceeds `maxBulkDeleteLength` limit

## Examples

**Soft Delete (preserve metadata):**

```bash
curl -X PUT ".../objects/obj_123/delete" -H "Authorization: Bearer token" \
  -d '{}'
# Both parameters default to false: metadata preserved, storage preserved
# Object returns 410 Gone on subsequent read/access requests
```

**Hard Delete (permanent, metadata and storage):**

```bash
curl -X PUT ".../objects/obj_456/delete" -H "Authorization: Bearer token" \
  -d '{"delete_object_metadata": true, "delete_storage_data": true}'
```

**Metadata Update (delete and re-register):**

```bash
curl -X PUT ".../objects/obj_123/delete" \
  -d '{"delete_object_metadata": true}'
curl -X POST ".../objects/register" \
  -d '{"candidates": [{"name": "updated.vcf", ...}]}'
```

**Bulk Delete (Atomic):**

```bash
curl -X PUT ".../objects/delete" -d '{
  "bulk_object_ids": ["obj_1", "obj_2"],
  "passports": ["..."],
  "delete_object_metadata": true,
  "delete_storage_data": true
}'
# All objects deleted or none deleted (transactional)
```

## Best Practices

**Clients:** Check service-info, default to safe deletion, handle transactional failures, respect limits, confirm destructive operations, do not rely on underlying storage deletion

**Servers:** Advertise capabilities, validate permissions, implement atomic transactions, implement limits, use versioning to avoid inadvertent deletion or critical data.

## Security Considerations

- **Authentication**: Validate GA4GH Passports and Bearer tokens
- **HTTPS Required**: Protect credentials in transit
- **Rate Limiting**: Prevent abuse of delete endpoints
- **Input Validation**: Sanitize all request parameters

## Backward Compatibility

Delete functionality is designed to be backward compatible:

- **No Impact on Existing Endpoints**: All existing DRS endpoints remain unchanged
- **Optional Implementation**: Servers can ignore delete functionality entirely
- **Graceful Degradation**: Clients receive 404 responses when delete is not supported
- **Safe Defaults**: New fields in service-info have safe default values, and requests default to leaving underlying data in place.
