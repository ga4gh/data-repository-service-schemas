## DRS IDs

Each implementation of DRS can choose its own id scheme, as long as it follows these guidelines:

* DRS IDs are strings made up of uppercase and lowercase letters, decimal digits, hyphen, period, underscore and tilde [A-Za-z0-9.-_~]. See [RFC 3986 § 2.3](https://datatracker.ietf.org/doc/html/rfc3986#section-2.3).
* DRS IDs can contain other characters, but they MUST be encoded into valid DRS IDs whenever they are used in API calls. This is because non-encoded IDs may interfere with the interpretation of the objects/{id}/access endpoint. To overcome this limitation use percent-encoding of the ID, see [RFC 3986 § 2.4](https://datatracker.ietf.org/doc/html/rfc3986#section-2.4)
* One DRS ID MUST always return the same object data (or, in the case of a collection, the same set of objects). This constraint aids with reproducibility.
* DRS implementations MAY have more than one ID that maps to the same object.
* DRS version 1.x does NOT support semantics around multiple versions of an object. (For example, there’s no notion of “get latest version” or “list all versions”.) Individual implementations MAY choose an ID scheme that includes version hints.

## DRS URIs

For convenience, including when passing content references to a [WES server](https://github.com/ga4gh/workflow-execution-service-schemas), we define a [URI scheme](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#Generic_syntax) for DRS-accessible content. This section documents the syntax of DRS URIs, and the rules clients follow for translating a DRS URI into a URL that they use for making the DRS API calls described in this spec.

There are two styles of DRS URIs, Hostname-based and Compact Identifier-based, both using the `drs://` URI scheme. DRS servers may choose either style when exposing references to their content;. DRS clients MUST support resolving both styles.

Tip:
> See [Appendix: Background Notes on DRS URIs](#tag/Background-Notes-on-DRS-URIs) for more information on our design motivations for DRS URIs.

### Hostname-based DRS URIs

Hostname-based DRS URIs are simpler than compact identifier-based URIs. They contain the DRS server name and the DRS ID only and can be converted directly into a fetchable URL based on a simple rule. They take the form:

```
drs://<hostname>/<id>
```

DRS URIs of this form mean *\"you can fetch the content with DRS id \<id\> from the DRS server at \<hostname\>\"*.
For example, here are the client resolution steps if the URI is:

```
drs://drs.example.org/314159
```

1. The client parses the string to extract the hostname of “drs.example.org” and the id of “314159”.
2. The client makes a GET request to the DRS server, using the standard DRS URL syntax:

```
GET https://drs.example.org/ga4gh/drs/v1/objects/314159
```

The protocol is always https and the port is always the standard 443 SSL port. It is invalid to include a different port in a DRS hostname-based URI.

Tip:
> See the [Appendix: Hostname-Based URIs](#tag/Hostname-Based-URIs) for information on how hostname-based DRS URI resolution to URLs is likely to change in the future, when the DRS v2 major release happens.

### Compact Identifier-based DRS URIs

Compact Identifier-based DRS URIs use resolver registry services (specifically, [identifiers.org](https://identifiers.org/) and [n2t.net (Name-To-Thing)](https://n2t.net/)) to provide a layer of indirection between the DRS URI and the DRS server name — the actual DNS name of the DRS server is not present in the URI. This approach is based on the Joint Declaration of Data Citation Principles as detailed by [Wimalaratne et al (2018)](https://www.nature.com/articles/sdata201829).

For more information, see the document [More Background on Compact Identifiers](./more-background-on-compact-identifiers.html).

Compact Identifiers take the form:

```
drs://[provider_code/]namespace:accession
```

Together, provider code and the namespace are referred to as the `prefix`. The provider code is optional and is used by identifiers.org/n2t.net for compact identifier resolver mirrors. Both the `provider_code` and `namespace` disallow spaces or punctuation, only lowercase alphanumerical characters, underscores and dots are allowed (e.g. [A-Za-z0-9._]).

Tip:
> See the [Appendix: Compact Identifier-Based URIs](#tag/Compact-Identifier-Based-URIs) for more background on Compact Identifiers and resolver registry services like identifiers.org/n2t.net (aka meta-resolvers), how to register prefixes, possible caching strategies, and security considerations.

#### For DRS Servers

If your DRS implementation will issue DRS URIs based *on your own* compact identifiers, you MUST first register a new prefix with identifiers.org (which is automatically mirrored to n2t.net). You will also need to include a provider resolver resource in this registration which links the prefix to your DRS server, so that DRS clients can get sufficient information to make a successful DRS GET request. For clarity, we recommend you choose a namespace beginning with `drs`.

#### For DRS Clients

A DRS client parses the DRS URI compact identifier components to extract the prefix and the accession, and then uses meta-resolver APIs to locate the actual DRS server. For example, here are the client resolution steps if the URI is:

```
drs://drs.42:314159
```

1. The client parses the string to extract the prefix of `drs.42` and the accession of `314159`, using the first occurrence of a colon (":") character after the initial `drs://` as a delimiter. (The colon character is not allowed in a Hostname-based DRS URI, making it easy to tell them apart.)

2. The client makes API calls to a meta-resolver to look up the URL pattern for the namespace. (See [Calling Meta-Resolver APIs for Compact Identifier-Based DRS URIs](#section/Calling-Meta-Resolver-APIs-for-Compact-Identifier-Based-DRS-URIs) for details.) The URL pattern is a string containing a `{$id}` parameter, such as:

```
https://drs.myexample.org/ga4gh/drs/v1/objects/{$id}
```

3. The client generates a DRS URL from the URL template by replacing {$id} with the accession it extracted in step 1. It then makes a GET request to the DRS server:

```
GET https://drs.myexample.org/ga4gh/drs/v1/objects/314159
```

4. The client follows any HTTP redirects returned in step 3, in case the resolver goes through an extra layer of redirection.

For performance reasons, DRS clients SHOULD cache the URL pattern returned in step 2, with a suggested 24 hour cache life.

### Choosing a URI Style

DRS servers can choose to issue either hostname-based or compact identifier-based DRS URIs, and can be confident that compliant DRS clients will support both. DRS clients must be able to accommodate both URI types. Tradeoffs that DRS server builders, and third parties who need to cite DRS objects in datasets, workflows or elsewhere, may want to consider include:

*Table 1: Choosing a URI Style*

|                   | Hostname-based | Compact Identifier-based |
|-------------------|----------------|--------------------------|
| URI Durability    | URIs are valid for as long as the server operator maintains ownership of the published DNS address. (They can of course point that address at different physical serving infrastructure as often as they would like.) | URIs are valid for as long as the server operator maintains ownership of the published compact identifier resolver namespace. (They also depend on the meta-resolvers like identifiers.org/n2t.net remaining operational, which is intended to be essentially forever.) |
| Client Efficiency | URIs require minimal client logic, and no network requests, to resolve. | URIs require small client logic, and 1-2 cacheable network requests, to resolve. |
| Security          | Servers have full control over their own security practices. | Server operators, in addition to maintaining their own security practices, should confirm they are comfortable with the resolver registry security practices, including protection against denial of service and namespace-hijacking attacks. (See the [Appendix: Compact Identifier-Based URIs](#tag/Compact-Identifier-Based-URIs) for more information on resolver registry security.) |

## DRS Datatypes
DRS's job is data access, period. Therefore, the DRS API supports a simple flat content model -- every `DrsObject`, like a file, represents a single opaque blob of bytes. DRS has no understanding of the meaning of objects and only provides simple domain-agnostic metadata. Understanding the semantics of specific object types is the responsibility of the applications that use DRS to fetch those objects (e.g. samtools for BAM files, DICOM viewers for DICOM objects).

### Atomic Objects
DRS can be used to access individual objects of all kinds, simple or complex, large or small, stored in type-specific formats (e.g. BAM files, VCF files, CSV files). At the API level these are all the same; at the application level, DRS clients and servers are expected to agree on object semantics using non-DRS mechanisms, including but not limited to the GA4GH Data Connect API.

### Compound Objects
DRS can also be used to access compound objects, consisting of two or more atomic objects related to each other in a well-specified way. See the [Appendix: Compound Objects](#tag/Compound-Objects) for suggested best practices for working with Compound Objects. 

### [DEPRECATED] Bundles
Previous versions of the DRS API spec included support for a *bundle* content type, which was a folder-like collection of other DRS objects (either blobs or bundles), represented by a `DrsObject` with a `contents` array. As of v1.3, bundles have been deprecated in favor of the best practices documented in the [Appendix: Compound Objects](#tag/Compound-Objects). A future version of the API spec may remove bundle support entirely.

## Read-only

DRS v1 is a read-only API. We expect that each implementation will define its own mechanisms and interfaces (graphical and/or programmatic) for adding and updating data.

## Standards

The DRS API specification is written in OpenAPI and embodies a RESTful service philosophy. It uses JSON in requests and responses and standard HTTPS on port 443 for information transport.  Optionally, it
supports authentication and authorization using the [GA4GH Passport](https://github.com/ga4gh-duri/ga4gh-duri.github.io/tree/master/researcher_ids) standard.
