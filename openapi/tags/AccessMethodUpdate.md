> Access method updates are an optional extension to the DRS API. Not all DRS servers implement them, and clients should check `/service-info` for `accessMethodUpdateSupported` before attempting to use these endpoints.

The access method update endpoints allow authorized clients to change how an existing DRS object can be accessed, without changing the object's core metadata such as its size, checksums, or name. This is useful when data is migrated between storage providers, when a mirror or an alternative protocol is added, or when a URL changes, in each case keeping the same DRS object ID.

An update overwrites the existing access methods for an object. A client that wants to add an access method while keeping the existing ones should first retrieve the object's current access methods and include them in the update request alongside the new method.

A single object is updated through `PUT /objects/{object_id}/access-methods`. Several objects can be updated together through `PUT /objects/access-methods`, which takes an `updates` array, each entry pairing an `object_id` with its new `access_methods`. Bulk updates are atomic: if any object fails, the whole request fails and none are updated.

A server MAY validate that the new access methods point to the same data, for example by checking file availability, checksums, or content. This behaviour is advertised in the `validateAccessMethods` field in `/service-info`.

## Service discovery

A server advertises its access method update capabilities in `/service-info`:

```json
{
  "drs": {
    "accessMethodUpdateSupported": true,
    "maxBulkAccessMethodUpdateLength": 100,
    "validateAccessMethods": false
  }
}
```

- `accessMethodUpdateSupported`: whether the server supports access method updates.
- `maxBulkAccessMethodUpdateLength`: the maximum number of objects in a single bulk update request.
- `validateAccessMethods`: whether the server validates new access methods.

## Examples

Updating the access methods of a single object, for example after migrating its data to a new bucket:

```bash
curl -X PUT "https://drs.example.org/objects/obj_123/access-methods" \
  -H "Content-Type: application/json" \
  -d '{
    "access_methods": [
      {"type": "s3", "access_url": {"url": "s3://new-bucket/migrated/file.bam"}}
    ]
  }'
```

Updating several objects atomically:

```bash
curl -X PUT "https://drs.example.org/objects/access-methods" \
  -H "Content-Type: application/json" \
  -d '{
    "updates": [
      {"object_id": "obj_1", "access_methods": [{"type": "https", "access_url": {"url": "https://new-location.com/file1.bam"}}]},
      {"object_id": "obj_2", "access_methods": [{"type": "s3", "access_url": {"url": "s3://new-bucket/file2.vcf"}}]}
    ]
  }'
```

GA4GH Passports may be supplied in the request body, and Bearer tokens in the `Authorization` header.

## Error responses

- `400`: the access methods are invalid, or validation failed.
- `401`: authentication is required.
- `403`: the client lacks permission for one or more objects in the request.
- `404`: an object was not found, or access method updates are not supported.
- `413`: a bulk request exceeds `maxBulkAccessMethodUpdateLength`.
