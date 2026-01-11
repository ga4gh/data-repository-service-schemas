# Access Method Updates

> **Optional Functionality**: Access method updates are optional extensions to the DRS API. Not all DRS servers implement this functionality. Clients should check `/service-info` for `accessMethodUpdateSupported` before attempting to use these endpoints.

Access method update endpoints allows authorized clients to modify how existing DRS objects can be accessed without changing the core object metadata (size, checksums, name). This is useful for storage migrations, adding mirrors, or updating URLs.

These endpoints will overwrite existing access methods for an object, if clients want to add access methods in addition to existing ones for objects they should first retrieve the current access methods and include them in the update request along with the new methods.

## Use Cases

- **Storage Migration**: Move data between storage providers while keeping same DRS object
- **Mirror Addition**: Add additional regional access points, or alternative protocols
- **URL Refresh**: Update changed domain names
- **Access Optimization**: Add or remove access methods based on performance or cost

## Design Principles

- **Optional**: Access method update support is completely optional
- **Immutable Core**: Only access methods can be updated - size, checksums, name remain unchanged
- **Atomic Bulk Operations**: All updates succeed or all fail (transactional)
- **Optional Validation**: Servers MAY validate new access methods point to same data
- **Flexible Authentication**: Supports GA4GH Passports, Bearer tokens, API keys

## Service Discovery

Check `/service-info` for access method update capabilities:

```json
{
  "drs": {
    "accessMethodUpdateSupported": true,
    "maxBulkAccessMethodUpdateLength": 100,
    "validateAccessMethods": false
  }
}
```

- **`accessMethodUpdateSupported`**: Whether the server supports access method updates
- **`maxBulkAccessMethodUpdateLength`**: Maximum objects per bulk update request
- **`validateAccessMethods`**: Whether the server validates access methods

## Single Object Update

Update access methods for a single DRS object:

```bash
curl -X PUT "https://drs.example.org/objects/obj_123/access-methods" \
  -H "Content-Type: application/json" \
  -d '{
    "access_methods": [
      {
        "type": "https",
        "access_url": {
          "url": "https://new-location.com/data/file.bam"
        }
      },
      {
        "type": "s3",
        "access_id": "s3,
        "access_url": {
          "url": "s3://new-bucket/migrated/file.bam"
        }
      }
    ]
  }'
```

## Bulk Object Update

Update access methods for multiple objects atomically:

```bash
curl -X PUT "https://drs.example.org/objects/access-methods" \
  -H "Content-Type: application/json" \
  -d '{
    "updates": [
      {
        "object_id": "obj_123",
        "access_methods": [
          {
            "type": "https",
            "access_url": {"url": "https://new-location.com/file1.bam"}
          }
        ]
      },
      {
        "object_id": "obj_456", 
        "access_methods": [
          {
            "type": "s3",
            "access_url": {"url": "s3://new-bucket/file2.vcf"}
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
  "access_methods": [...],
  "passports": ["eyJhbGci..."]
}
```

**Bearer Tokens** (in headers):

```bash
curl -H "Authorization: Bearer token" -d '{"access_methods": [...]}' ...
```

## Validation

Servers MAY validate that new access methods point to the same data by checking file availability, checksums or file content. Validation behavior is advertised in `validateAccessMethods` service-info field.

## Error Responses

- **400**: Invalid access methods or validation failure
- **401**: Authentication required
- **403**: Insufficient permissions for object(s)
- **404**: Object not found or access method updates not supported
- **413**: Bulk request exceeds `maxBulkAccessMethodUpdateLength` limit

## Examples

**Storage Migration:**

```bash
# Update single object after migration
curl -X PUT "https://drs.example.org/objects/obj_123/access-methods" \
  -d '{"access_methods": [{"type": "s3", "access_url": {"url": "s3://new-bucket/file.bam"}}]}'
```

**Bulk Migration:**

```bash
# Migrate multiple objects atomically
curl -X PUT "https://drs.example.org/objects/access-methods" \
  -d '{
    "updates": [
      {"object_id": "obj_1", "access_methods": [...]},
      {"object_id": "obj_2", "access_methods": [...]}
    ]
  }'
```

## Best Practices

**Clients**: Check service-info first, handle atomic transaction failures, respect bulk limits, verify permissions

**Servers**: Advertise capabilities clearly, implement atomic transactions for bulk operations, validate permissions, consider optional validation for data integrity

## Backward Compatibility

Access method update functionality is designed to be backward compatible:

- **No Impact on Existing Endpoints**: All existing DRS endpoints remain unchanged
- **Optional Implementation**: Servers can ignore this functionality entirely  
- **Graceful Degradation**: Clients receive 404 responses when not supported
- **Safe Defaults**: New service-info fields have safe default values
