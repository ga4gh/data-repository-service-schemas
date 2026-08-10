> Delete support is an optional extension to the DRS API. Not all DRS servers implement it, and clients should check `/service-info` for the relevant capability flags before attempting to use the delete endpoints.

DRS delete functionality allows suitably authenticated clients to request that DRS objects are removed from the server and, optionally, that the server attempt to delete the underlying data. Because delete support is optional, servers operating in untrusted environments may choose not to support it at all, and servers should ensure that they trust the clients from whom they accept delete requests.

Delete uses an HTTP `PUT` rather than `DELETE`, because GA4GH Passports are passed in a request body and `DELETE` does not reliably support request bodies across all HTTP infrastructure.

The delete endpoints accept two independent parameters, `delete_object_metadata` and `delete_storage_data`, which control what is removed. Both default to the safest option, leaving data in place.

## Deleting object metadata

The `delete_object_metadata` parameter controls whether the DRS object metadata record is permanently removed or preserved. It defaults to `false`.

When `delete_object_metadata` is `false`, the server marks the object as deleted but preserves the metadata record, a mode known as soft deletion. Read and access requests for a soft-deleted object return `410 Gone` with a standard `Error` response body. This mode requires `metadataRetentionSupported` to be `true` in `/service-info`; a server that does not support metadata retention silently ignores the parameter and permanently deletes the metadata.

When `delete_object_metadata` is `true`, the server permanently removes the metadata record. The object ID no longer resolves and cannot be recovered.

## Deleting underlying data

The `delete_storage_data` parameter lets a client express a preference that the underlying data referred to by the deleted object is also removed. It defaults to `false`, leaving the underlying data in place. A server advertises whether it supports the parameter at all with the `deleteStorageDataSupported` flag.

Servers are free to interpret the request as they choose. A server that attempts to honour it need not do so synchronously, and may, for example, register the file for later deletion or implement soft deletion with versioning. A server may also choose to confirm that no other DRS object refers to the same underlying data before deleting it. Where an object refers to data held in more than one backend, for example where it has multiple `access_methods`, the server may delete the data from all or only some of those backends. A server may also lack the permissions needed to delete the data, or encounter errors when it tries.

For these reasons clients MUST NOT depend on the underlying data being deleted, even where the server advertises `deleteStorageDataSupported` and the client sets `delete_storage_data`. HTTP responses indicate metadata deletion status only, and storage deletion is always a best-effort attempt.

## Bulk deletion

The `/objects/delete` endpoint deletes several objects in one request. Servers SHOULD treat this as an atomic transaction: if any object fails validation or deletion, the whole request fails, no objects are deleted, and no attempt is made to delete underlying storage for any object. A server MAY instead perform partial deletion with appropriate error reporting where atomic behaviour is not feasible. A successful bulk delete returns `204 No Content`, and the failure of an atomic request returns a `4xx` error and leaves all objects in place.

## Updating objects through delete and re-registration

Rather than introducing separate update operations, which would complicate server implementation, a metadata-only delete combined with the `/objects/register` endpoint gives clients a way to update DRS metadata without affecting the underlying data. A client deletes the existing metadata and registers a new object with the corrected metadata. An object's `access_methods` and additional checksums can be changed while keeping the same DRS object ID, as described in the access method update and checksum addition sections, but any other change requires deletion and re-registration under a new ID. Where the DRS server controls the storage backend, this offers a convenient, vendor-neutral way for clients to update and delete both objects and their data.

## Service discovery

A server advertises its delete capabilities in `/service-info`:

```json
{
  "drs": {
    "deleteSupported": true,
    "maxBulkDeleteLength": 100,
    "deleteStorageDataSupported": true,
    "metadataRetentionSupported": true
  }
}
```

- `deleteSupported`: whether the server supports deletion.
- `maxBulkDeleteLength`: the maximum number of objects in a single bulk delete request.
- `deleteStorageDataSupported`: whether the server can attempt to delete underlying storage data.
- `metadataRetentionSupported`: whether the server can preserve metadata after deletion, that is soft delete via `delete_object_metadata: false`.

## Examples

A soft delete, preserving both the metadata record and the underlying storage, since both parameters default to `false`:

```bash
curl -X PUT ".../objects/obj_123/delete" -H "Authorization: Bearer token" -d '{}'
# Object returns 410 Gone on subsequent read and access requests
```

A permanent delete of the metadata together with an attempt to delete the storage:

```bash
curl -X PUT ".../objects/obj_456/delete" -H "Authorization: Bearer token" \
  -d '{"delete_object_metadata": true, "delete_storage_data": true}'
```

A bulk delete, which is atomic:

```bash
curl -X PUT ".../objects/delete" -d '{
  "bulk_object_ids": ["obj_1", "obj_2"],
  "passports": ["..."],
  "delete_object_metadata": true,
  "delete_storage_data": true
}'
# All objects are deleted, or none are
```

GA4GH Passports may be supplied in the request body, and Bearer tokens in the `Authorization` header.

## Error responses

- `400`: storage deletion is not supported, or the request parameters are invalid.
- `403`: the client lacks permission for one or more objects in the request.
- `404`: an object was not found, or the delete endpoints are not supported.
- `413`: a bulk request exceeds `maxBulkDeleteLength`.
