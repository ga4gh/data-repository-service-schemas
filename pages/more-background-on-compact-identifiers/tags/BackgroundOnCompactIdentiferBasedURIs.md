Compact identifiers refer to locally-unique persistent identifiers that have been namespaced to provide global uniqueness. See ["Uniform resolution of compact identifiers for biomedical data"](https://www.biorxiv.org/content/10.1101/101279v3) for an excellent introduction to this topic. By using compact identifiers in DRS URIs, along with a resolver registry (identifiers.org/n2t.net), systems can identify the current resolver when they need to translate a DRS URI into a fetchable URL. This allows a project to issue compact identifiers in DRS URIs and not be concerned if the project name or DRS hostname changes in the future, the current resolver can always be found through the identifiers.org/n2t.net registries. Together the identifiers.org/n2t.net systems support the resolver lookup for over 700 compact identifiers formats used in the research community, making it possible for a DRS server to use any of these as DRS IDs (or to register a new compact identifier type and resolver service of their own).

We use a DRS URI scheme rather than [Compact URIs (CURIEs)](https://en.wikipedia.org/wiki/CURIE) directly since we feel that systems consuming DRS objects will be able to better differentiate a DRS URI. CURIEs are widely used in the research community, and we feel the fact that they can point to a wide variety of entities (HTML documents, PDFs, identities in data models, etc) makes it more difficult for systems to unambiguously identify entities as DRS objects.

Still, to make compact identifiers work in DRS URIs we leverage the CURIE format used by identifiers.org/n2t.net. Compact identifiers have the form:

```
prefix:accession
```

The prefix can be divided into a `provider_code` (optional) and `namespace`. The `accession` here is an Ark, DOI, Data GUID, or another issuer's local ID for the object being pointed to:

```
[provider_code/]namespace:accession
```

Both the `provider_code` and `namespace` disallow spaces or punctuation, only lowercase alphanumerical characters, underscores and dots are allowed.

[Examples](https://n2t.net/e/compact_ids.html) include (from n2t.net):

```
PDB:2gc4
Taxon:9606
DOI:10.5281/ZENODO.1289856
ark:/47881/m6g15z54
IGSN:SSH000SUA
```

Tip:
> DRS URIs using compact identifiers with resolvers registered in identifiers.org/n2t.net can be distinguished from the hostname-based DRS URIs below based on the required ":" which is not allowed in hostname-based URI.

See the documentation on [n2t.net](https://n2t.net/e/compact_ids.html) and [identifiers.org](https://docs.identifiers.org/) for much more information on the compact identifiers used there and details about the resolution process.
