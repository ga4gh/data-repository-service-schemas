A DRS client identifies the a DRS URI compact identifier components using the first occurance of "/" (optional) and ":" characters. These are not allowed inside the provider_code (optional) or the namespace. The ":" character is not allowed in a Hostname-based DRS URI, providing a convenient mechanism to differentiate them. Once the provider_code (optional) and namespace are extracted from a DRS compact identifier-based URI, a client can use services on identifiers.org to identify available resolvers.

*Let’s look at a specific example DRS compact identifier-based URI that uses DOIs, a popular compact identifier, and walk through the process that a client would use to resolve it. Keep in mind, the resolution process is the same from the client perspective if a given DRS server is using an existing compact identifier type (DOIs, ARKs, Data GUIDs) or creating their own compact identifier type for their DRS server and registering it on identifiers.org/n2t.net.*

Starting with the DRS URI:

```
drs://doi:10.5072/FK2805660V
```

with a namespace of "doi", the following GET request will return information about the namespace:

```
GET https://registry.api.identifiers.org/restApi/namespaces/search/findByPrefix?prefix=doi
```

This information then points to resolvers for the "doi" namespace. This "doi" namespace was assigned a namespace ID of 75 by identifiers.org. This "id" has nothing to do with compact identifier accessions (which are used in the URL pattern as `{$id}` below) or DRS IDs. This namespace ID (75 below) is purely an identifiers.org internal ID for use with their APIs:

```
GET https://registry.api.identifiers.org/restApi/resources/search/findAllByNamespaceId?id=75
```

This returns enough information to, ultimately, identify one or more resolvers and each have a URL pattern that, for DRS-supporting systems, provides a URL template for making a successful DRS GET request. For example, the DOI urlPattern is:

```
urlPattern: "https://doi.org/{$id}"
```

And the `{$id}` here refers to the accession from the compact identifier (in this example the accession is `10.5072/FK2805660V`). If applicable, a provide code can be supplied in the above requests to specify a particular mirror if there are multiple resolvers for this namespace. In the case of DOIs, you only get a single resolver.

Given this information you now know you can make a GET on the URL:

```
GET https://doi.org/10.5072/FK2805660V
```

*The URL above is valid for a DOI object but it is not actually a DRS server! Instead, it redirects to a DRS server through a series of HTTPS redirects. This is likely to be common when working with existing compact identifiers like DOIs or ARKs. Regardless, the redirect should eventually lead to a DRS URL that percent-encodes the accession as a DRS ID in a DRS object API call. For a **hypothetical** example, here’s what a redirect to a DRS API URL might ultimately look. A client doesn’t have to do anything other than follow the HTTPS redirects. The link between the DOI resolver on doi.org and the DRS server URL below is the result of the DRS server registering their data objects with a DOI issuer.*

```
GET https://drs.example.org/ga4gh/drs/v1/objects/10.5072%2FFK2805660V
```

IDs in DRS hostname-based URIs/URLs are always percent-encoded to eliminate ambiguity even though the DRS compact identifier-based URIs and the identifier.orgs API do not percent-encode accessions. This was done in order to 1) follow the CURIE conventions of identifiers.org/n2t.net for compact identifier-based DRS URIs and 2) to aid in readability for users who understand they are working with compact identifiers. **The general rule of thumb, when using a compact identifier accession as a DRS ID in a DRS API call, make sure to percent-encode it. An easy way for a DRS client to handle this is to get the initial DRS object JSON response from whatever redirects the compact identifier resolves to, then look for the** `self_uri` **in the JSON, which will give you the correctly percent-encoded DRS ID for subsequent DRS API calls such as the** `access` **method.**
