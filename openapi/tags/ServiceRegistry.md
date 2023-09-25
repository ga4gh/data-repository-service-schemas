The [GA4GH Service Registry API specification](https://github.com/ga4gh-discovery/ga4gh-service-registry) allows information about GA4GH-compliant web services, including DRS services, to be aggregated into registries and made available via a standard API. The following considerations should be followed when registering DRS services within a service registry.

* The DRS service attributes returned by `/service-info` (i.e. `id`, `name`, `description`, etc.) should have the same values as the registry entry for that service.
* The value of the `type` object's `artifact` property should be `drs` (i.e. the same as it appears in `service-info`)
* Each entry in a Service Registry must have a `url`, indicating the base URL to the web service. For DRS services, the registered `url` must include everything up to
the standardized `/ga4gh/drs/v1` path. Clients should be able to assume that:
    + Adding `/ga4gh/drs/v1/objects/{object_id}` to the registered `url` will hit the `DrsObject` endpoint
    + Adding `/ga4gh/drs/v1/service-info` to the registered `url` will hit the Service Info endpoint

Example listing of a DRS API registration from a service registry's `/services` endpoint:

```
[
    {
        "id": "com.example.drs",
        "name": "Example DRS API",
        "type": {
            "group": "org.ga4gh",
            "artifact": "drs",
            "version": "1.4.0"
        },
        "description": "The Data Repository Service (DRS) API ...",
        "organization": {
            "id": "com.example",
            "name": "Example Company"
        },
        "contactUrl": "mailto:support@example.com",
        "documentationUrl": "https://docs.example.com/docs/drs",
        "createdAt": "2021-08-09T00:00:00Z",
        "updatedAt": "2021-08-09T12:30:00Z",
        "environment": "production",
        "version": "1.13.4",
        "url": "https://drs-service.example.com"
    }
]
```
