## Encoding DRS IDs

In hostname-based DRS URIs, the ID is always percent-encoded to ensure special characters do not interfere with subsequent DRS endpoint calls. As such, ":" is not allowed in the URI and is a convenient way of differentiating from a compact identifier-based DRS URI. Also, if a given DRS service implementation uses compact identifier accessions as their DRS IDs, they must be percent encoded before using them as DRS IDs in hostname-based DRS URIs and subsequent GET requests to a DRS service endpoint.

## Future DRS Versions and Service Registry/Info

In the future, as new major versions of DRS are released, a DRS server might support multiple API versions on different URL paths. At that point we expect to add support for [service-registry](https://github.com/ga4gh-discovery/ga4gh-service-registry) and [service-info](https://github.com/ga4gh-discovery/ga4gh-service-info) endpoints to the API, and to update the URI resolution logic to describe how to use those endpoints when translating hostname-based DRS URIs to URLs.
