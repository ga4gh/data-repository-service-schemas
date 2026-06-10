> Checksum addition is an optional extension to the DRS API. Not all DRS servers implement it, and clients should check `/service-info` for `checksumAdditionSupported` before attempting to use these endpoints.

The checksum addition endpoints allow authorized clients to add further checksums to an existing DRS object. This is useful for a server that relies on a particular checksum type, such as SHA-256, where objects are not guaranteed to carry that checksum when they are created, for example where they are registered with an MD5 checksum only.

These endpoints only add checksums. A client SHOULD NOT attempt to change the value of an existing checksum or to remove one, and a server MUST NOT change any existing checksum. If a client attempts to update an existing checksum the server's behaviour is implementation dependent: it MAY ignore the request, or MAY return a `4XX` error. If an incorrect checksum has been registered, the client should delete the existing DRS object, where the server supports deletion, and register a new object with the correct metadata. This ensures that a single DRS object ID always points to the same object.

A single object is updated through `PUT /objects/{object_id}/checksums`. Several objects can be updated together through `PUT /objects/checksums`, which takes an `additions` array, each entry pairing an `object_id` with the `checksums` to add. Bulk additions are atomic: if any object fails, the whole request fails and none are updated. A server MAY validate that the new checksums match the underlying object, a behaviour advertised in the `validateChecksums` field in `/service-info`.

## Service discovery

A server advertises its checksum addition capabilities in `/service-info`:

```json
{
  "drs": {
    "checksumAdditionSupported": true,
    "maxBulkChecksumAdditionLength": 100,
    "validateChecksums": true
  }
}
```

- `checksumAdditionSupported`: whether the server supports checksum addition.
- `maxBulkChecksumAdditionLength`: the maximum number of objects in a single bulk addition request.
- `validateChecksums`: whether the server validates new checksums.

## Examples

Adding a SHA-256 checksum to an object that was registered with an MD5 checksum only:

```bash
curl -X PUT "https://drs.example.org/objects/obj_123/checksums" \
  -H "Content-Type: application/json" \
  -d '{
    "checksums": [
      {"checksum": "2320831154385267afee81d0d837473280117763f4acd426b3735c37a0500482", "type": "sha256"}
    ]
  }'
```

Adding checksums to several objects atomically:

```bash
curl -X PUT "https://drs.example.org/objects/checksums" \
  -H "Content-Type: application/json" \
  -d '{
    "additions": [
      {"object_id": "obj_123", "checksums": [{"checksum": "2320831154385267afee81d0d837473280117763f4acd426b3735c37a0500482", "type": "sha256"}]},
      {"object_id": "obj_456", "checksums": [{"checksum": "23d50c6804a8b198f7fe4ff11d4518fb46d8d8d1337c6b9aa0fbad7bb90b3d32", "type": "sha256"}]}
    ]
  }'
```

GA4GH Passports may be supplied in the request body, and Bearer tokens in the `Authorization` header.

## Error responses

- `400`: the checksums are invalid, or validation failed.
- `401`: authentication is required.
- `403`: the client lacks permission for one or more objects in the request.
- `404`: an object was not found, or checksum additions are not supported.
- `413`: a bulk request exceeds `maxBulkChecksumAdditionLength`.
