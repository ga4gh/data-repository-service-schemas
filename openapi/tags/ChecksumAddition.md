# Add additional checksum

> **Optional Functionality**: Checksum additions are optional extensions to the DRS API.
Not all DRS servers are required to implement this functionality. Clients should check
`/service-info` for `checksumAdditionSupported` before attempting to use these endpoints.

Checksum addition endpoints allows authorized clients to add additional checksums to existing
DRS objects. This is useful for servers that rely on objects using a specific checksum type,
e.g. SHA-256, and where objects are not guaranteed to have this checksum at creation time, e.g.
objects may be created with an MD5 checksum only. The server MAY choose to validate checksums
and return errors for mismatches, this behaviour is advertised in the `validateChecksums`
field in `/service-info`.

These endpoints only support the addition of additional checksums, a client SHOULD NOT
attempt to update the value of an existing checksum or to remove a checksum. If a client
attempts to update an existing checksum the server behaviour is implementation
dependent but servers MAY simply ignore the request, or MAY return a 4XX error to the client.
Servers MUST NOT change any existing checksums. If an incorrect checksum has been registered
then clients should delete the existing DRS object (if supported by the server) and register
a new DRS object with the correct metadata. This ensures that a single DRS object ID _always_
points to the same object.

## Design Principles

- **Optional**: Checksum addition support is completely optional
- **Object Immutability**: Existing checksums cannot be changed
- **Atomic Bulk Operations**: All additions succeed or all fail (transactional)
- **Flexible Authentication**: Supports GA4GH Passports, Bearer tokens, API keys

## Service Discovery

Check `/service-info` for checksum addition capabilities:

```json
{
  "drs": {
    "checksumAdditionSupported": true,
    "maxBulkChecksumAdditionLength": 100,
    "validateChecksums": true
  }
}
```

- **`checksumAdditionSupported`**: Whether server supports checksum addition
- **`maxBulkChecksumAdditionLength`**: Maximum objects per bulk addition request
- **`validateChecksums`**: Whether server validates new checksums

## Single Object Checksum Addition

Add checksum for a single DRS object:

```bash
curl -X PUT "https://drs.example.org/objects/obj_123/checksums" \
  -H "Content-Type: application/json" \
  -d '{
    "checksums": [
      {
        "checksum": "2320831154385267afee81d0d837473280117763f4acd426b3735c37a0500482",
        "type": "sha256"
      }
    ]
  }'
```

## Bulk Object Checksum Addition

Add checksums for multiple objects atomically:

```bash
curl -X PUT "https://drs.example.org/objects/checksums" \
  -H "Content-Type: application/json" \
  -d '{
    "additions": [
      {
        "object_id": "obj_123",
        "checksums": [
          {
            "checksum": "2320831154385267afee81d0d837473280117763f4acd426b3735c37a0500482",
            "type": "sha256"
          }
        ]
      },
      {
        "object_id": "obj_456", 
        "checksums": [
          {
            "checksum": "23d50c6804a8b198f7fe4ff11d4518fb46d8d8d1337c6b9aa0fbad7bb90b3d32",
            "type": "sha256"
          }
        ]
      }
    ]
  }'
```

## Authentication

**GA4GH Passports** (in request body):

```json
{
  "additions": [...],
  "passports": ["eyJhbGci..."]
}
```

**Bearer Tokens** (in headers):

```bash
curl -H "Authorization: Bearer token" -d '{"additions": [...]}' ...
```

## Validation

Servers MAY validate that new checksums match the underlying objects, this behaviour is
advertised in the `validateChecksums` service-info field.

## Error Responses

- **400**: Invalid checksums or validation failure
- **401**: Authentication required
- **403**: Insufficient permissions for object(s)
- **404**: Object not found or checksum additions not supported
- **413**: Bulk request exceeds `maxBulkChecksumAdditionLength` limit

## Examples

**Add SHA-256 checksum to an object that only has MD5:**

```bash
curl -X PUT "https://drs.example.org/objects/obj_123/checksums" \
  -H "Content-Type: application/json" \
  -d '{
    "checksums": [
      {
        "checksum": "2320831154385267afee81d0d837473280117763f4acd426b3735c37a0500482",
        "type": "sha256"
      }
    ]
  }'
```

**Bulk add checksums for multiple objects:**

```bash
curl -X PUT "https://drs.example.org/objects/checksums" \
  -H "Content-Type: application/json" \
  -d '{
    "additions": [
      {
        "object_id": "obj_123",
        "checksums": [{"checksum": "abc123...", "type": "sha256"}]
      },
      {
        "object_id": "obj_456",
        "checksums": [{"checksum": "def456...", "type": "sha256"}]
      }
    ]
  }'
```

## Best Practices

**Clients**: Check service-info first, handle atomic transaction failures, respect bulk limits, verify permissions

**Servers**: Advertise capabilities clearly, implement atomic transactions for bulk operations, validate permissions, consider optional validation for data integrity

## Backward Compatibility

Checksum addition functionality is designed to be backward compatible:

- **No Impact on Existing Endpoints**: All existing DRS endpoints remain unchanged
- **Optional Implementation**: Servers can ignore this functionality entirely  
- **Graceful Degradation**: Clients receive 404 responses when not supported
