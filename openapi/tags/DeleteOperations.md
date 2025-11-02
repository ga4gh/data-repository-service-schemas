# Delete Operations

Optional DRS functionality for removing objects and, optionally, data from the underlying storage service. Servers remain fully compliant without implementing delete endpoints.

## Overview

- **Optional**: Delete support is completely optional
- **Safe by Default**: Preserves storage data unless explicitly requested
- **Backward Compatible**: No impact on existing DRS functionality
- **Flexible Auth**: Supports GA4GH Passports and Bearer tokens

## Service Discovery

Check `/service-info` for delete capabilities:

```json
{
  "drs": {
    "deleteSupported": true,
    "maxBulkDeleteLength": 100,
    "deleteStorageDataSupported": true
  }
}
```

- **`deleteSupported`**: Whether server implements delete endpoints
- **`maxBulkDeleteLength`**: Maximum objects per bulk delete request  
- **`deleteStorageDataSupported`**: Whether server can attempt to delete underlying storage files

## Delete Endpoints

**Why POST instead of DELETE?** GA4GH Passports require request bodies, which DELETE methods don't reliably support across all HTTP infrastructure. POST ensures broad compatibility.

### Single Object Delete: `POST /objects/{object_id}/delete`

```bash
curl -X POST "https://drs.example.org/objects/drs_object_123456/delete" \
  -H "Content-Type: application/json" \
  -d '{"passports": ["..."], "delete_storage_data": false}'
# Response: 204 No Content (indicates metadata deletion success only)
```

**Note**: HTTP responses indicate metadata deletion status only. Storage deletion (`delete_storage_data: true`) is a best effort attempt with no guarantee of success.

### Bulk Object Delete: `POST /objects/delete`

```bash
curl -X POST "https://drs.example.org/objects/delete" \
  -H "Content-Type: application/json" \
  -d '{
    "bulk_object_ids": ["obj_1", "obj_2", "obj_3"],
    "passports": ["..."],
    "delete_storage_data": false
  }'
# Response: 204 No Content (all metadata deleted) or 207 Multi-Status (mixed metadata results)
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

## Storage Data Control

**`delete_storage_data: false`** (default): Removes metadata only, preserves storage files
**`delete_storage_data: true`**: Removes metadata AND attempts to delete storage files (requires server support, not guaranteed)

## Update Pattern

**Why no native updates?** DRS promotes immutability, data safety, and clear audit trails through explicit operations. This approach also makes implementation simpler by reusing existing endpoints.

**Safe Update Process:**
1. Delete metadata only: `POST /objects/{id}/delete` with `delete_storage_data: false`
2. Re-register object: `POST /objects/{id}` with updated metadata

```bash
# Delete metadata (preserves storage)
curl -X POST ".../objects/obj_123/delete" -d '{"delete_storage_data": false}'
# Re-register with updates
curl -X POST ".../objects/obj_123" -d '{"name": "updated.txt", ...}'
```

## Error Responses

- **400**: Unsupported storage deletion
- **403**: Insufficient permissions  
- **404**: Object not found or delete not supported
- **413**: Bulk request too large

## Examples

**Metadata Update:**
```bash
curl ".../service-info"  # Check capabilities
curl -X POST ".../objects/obj_123/delete" -d '{"delete_storage_data": false}'
curl -X POST ".../objects/obj_123" -d '{"name": "updated.vcf", ...}'
```

**Complete Removal:**
```bash
curl -X POST ".../objects/obj_456/delete" -H "Authorization: Bearer token" \
  -d '{"delete_storage_data": true}'
```

**Bulk Delete:**
```bash
curl -X POST ".../objects/delete" -d '{
  "bulk_object_ids": ["obj_1", "obj_2"],
  "passports": ["..."],
  "delete_storage_data": false
}'
```

## Best Practices

**Clients:** Check service-info, default to safe deletion, handle errors, respect limits, confirm destructive operations

**Servers:** Advertise capabilities, validate permissions, implement limits, audit logging, rate limiting

## Security Considerations

- **Authentication**: Validate GA4GH Passports and Bearer tokens
- **HTTPS Required**: Protect credentials in transit
- **Rate Limiting**: Prevent abuse of delete endpoints
- **Input Validation**: Sanitize all request parameters

## Backward Compatibility

Delete functionality is designed to be 100% backward compatible:

- **No Impact on Existing Endpoints**: All existing DRS endpoints remain unchanged
- **Optional Implementation**: Servers can ignore delete functionality entirely
- **Graceful Degradation**: Clients receive 404 responses when delete is not supported
- **Safe Defaults**: New fields in service-info have safe default values