**Note: Identifiers.org/n2t.net API Changes**

The examples below show the current API interactions with [n2t.net](https://n2t.net/e/compact_ids.html) and [identifiers.org](https://docs.identifiers.org/) which may change over time. Please refer to the documentation from each site for the most up-to-date information. We will make best efforts to keep the DRS specification current but DRS clients MUST maintain their ability to use either the identifiers.org or n2t.net APIs to resolve compact identifier-based DRS URIs.

## Registering a DRS Server on a Meta-Resolver

See the documentation on the [n2t.net](https://n2t.net/e/compact_ids.html) and [identifiers.org](https://docs.identifiers.org/) meta-resolvers for adding your own compact identifier type and registering your DRS server as a resolver. You can register new prefixes (or mirrors by adding resource provider codes) for free using a simple online form. For more information see [More Background on Compact Identifiers](./more-background-on-compact-identifiers.html).

## Calling Meta-Resolver APIs for Compact Identifier-Based DRS URIs

Clients resolving Compact Identifier-based URIs need to convert a prefix (e.g. “drs.42”) into a URL pattern. They can do so by calling either the identifiers.org or the n2t.net API, since the two meta-resolvers keep their mapping databases in sync.

### Calling the identifiers.org API as a Client

It takes two API calls to get the URL pattern.

1. The client makes a GET request to identifiers.org to find information about the prefix:

```
GET https://registry.api.identifiers.org/restApi/namespaces/search/findByPrefix?prefix=drs.42
```

This request returns a JSON structure including various URLs containing an embedded namespace id, such as:

```
"namespace" : {
  "href":"https://registry.api.identifiers.org/restApi/namespaces/1234"
}
```

2. The client extracts the namespace id (in this example 1234), and uses it to make a second GET request to identifiers.org to find information about the namespace:

```
GET https://registry.api.identifiers.org/restApi/resources/search/findAllByNamespaceId?id=1234
```

This request returns a JSON structure including an urlPattern field, whose value is a URL pattern containing a ${id} parameter, such as:

```
"urlPattern" : "https://drs.myexample.org/ga4gh/drs/v1/objects/{$id}"
```

### Calling the n2t.net API as a Client

It takes one API call to get the URL pattern.

The client makes a GET request to n2t.net to find information about the namespace. (Note the trailing colon.)

```
GET https://n2t.net/drs.42:
```

This request returns a text structure including a redirect field, whose value is a URL pattern containing an `$id` parameter, such as:

```
redirect: https://drs.myexample.org/ga4gh/drs/v1/objects/$id
```

## Caching with Compact Identifiers

Identifiers.org/n2t.net compact identifier resolver records do not change frequently. This reality is useful for caching resolver records and their URL patterns for performance reasons. Builders of systems that use compact identifier-based DRS URIs should cache prefix resolver records from identifiers.org/n2t.net and occasionally refresh the records (such as every 24 hours). This approach will reduce the burden on these community services since we anticipate many DRS URIs will be regularly resolved in workflow systems. Alternatively, system builders may decide to directly mirror the registries themselves, instructions are provided on the identifiers.org/n2t.net websites.

## Security with Compact Identifiers

As mentioned earlier, identifiers.org/n2t.net performs some basic verification of new prefixes and provider code mirror registrations on their sites. However, builders of systems that consume and resolve DRS URIs may have certain security compliance requirements and regulations that prohibit relying on an external site for resolving compact identifiers. In this case, systems under these security and compliance constraints may wish to whitelist certain compact identifier resolvers and/or vet records from identifiers.org/n2t.net before enabling in their systems.

## Accession Encoding to Valid DRS IDs

The compact identifier format used by identifiers.org/n2t.net does not percent-encode reserved URI characters but, instead, relies on the first ":" character to separate prefix from accession. Since these accessions can contain any characters, and characters like "/" will interfere with DRS API calls, you *must* percent encode the accessions extracted from DRS compact identifier-based URIs when using as DRS IDs in subsequent DRS GET requests. An easy way for a DRS client to handle this is to get the initial DRS object JSON response from whatever redirects the compact identifier resolves to, then look for the `self_uri` in the JSON, which will give you the correctly percent-encoded DRS ID for subsequent DRS API calls such as the `access` method.

## Additional Examples

For additional examples, see the document [More Background on Compact Identifiers](./more-background-on-compact-identifiers.html).
