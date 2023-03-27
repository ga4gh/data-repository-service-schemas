See the documentation on [n2t.net](https://n2t.net/e/compact_ids.html) and [identifiers.org](https://docs.identifiers.org/) for adding your own compact identifier type and registering your DRS server as a resolver. We document this in more detail in the [main specification document](./index.html).

Now the question is how does a client resolve your newly registered compact identifier for your DRS server? *It turns out, whether specific to a DRS implementation or using existing compact identifiers like ARKs or DOIs, the DRS client resolution process for compact identifier-based URIs is exactly the same.* We briefly run through process below for a new compact identifier as an example but, again, a client will not need to do anything different from the resolution process documented in "DRS Client Compact Identifier-Based URI Resolution Process - Existing Compact Identifier Provider".

Now we can issue DRS URI for our data objects like:

```
drs://mydrsprefix:12345
```

This is a little simpler than working with DOIs or other existing compact identifier issuers out there since we can create our own IDs and not have to allocate them through a third-party service (see "Issuing Existing Compact Identifiers for Use with Your DRS Server" below).

With a namespace of "mydrsprefix", the following GET request will return information about the namespace:

```
GET https://registry.api.identifiers.org/restApi/namespaces/search/findByPrefix?prefix=mydrsprefix
```

*Of course, this is a hypothetical example so the actual API call won’t work but you can see the GET request is identical to "DRS Client Compact Identifier-Based URI Resolution Process - Existing Compact Identifier Provider".*

This information then points to resolvers for the "mydrsprefix" namespace. Hypothetically, this "mydrsprefix" namespace was assigned a namespace ID of 1829 by identifiers.org. This "id" has nothing to do with compact identifier accessions (which are used in the URL pattern as `{$id}` below) or DRS IDs. This namespace ID (1829 below) is purely an identifiers.org internal ID for use with their APIs:

```
GET https://registry.api.identifiers.org/restApi/resources/search/findAllByNamespaceId?id=1829
```

*Like the previous GET request this URL won’t work but you can see the GET request is identical to "DRS Client Compact Identifier-Based URI Resolution Process - Existing Compact Identifier Provider".*

This returns enough information to, ultimately, identify one or more resolvers and each have a URL pattern that, for DRS-supporting systems, provides a URL template for making a successful DRS GET request. For example, the "mydrsprefix" urlPattern is:

```
urlPattern: "https://mydrs.server.org/ga4gh/drs/v1/objects/{$id}"
```

And the `{$id}` here refers to the accession from the compact identifier (in this example the accession is `12345`). If applicable, a provide code can be supplied in the above requests to specify a particular mirror if there are multiple resolvers for this namespace.

Given this information you now know you can make a GET on the URL:

```
GET https://mydrs.server.org/ga4gh/drs/v1/objects/12345
```

So, compared to using a third party service like DOIs and ARKs, this would be a direct pointer to a DRS server. However, just as with "DRS Client Compact Identifier-Based URI Resolution Process - Existing Compact Identifier Provider", the client should always be prepared to follow HTTPS redirects.

*To summarize, a client resolving a custom compact identifier registered for a single DRS server is actually the same as resolving using a third-party compact identifier service like ARKs or DOIs with a DRS server, just make sure to follow redirects in all cases.*

**Note: Issuing Existing Compact Identifiers for Use with Your DRS Server**

See the documentation on [n2t.net](https://n2t.net/e/compact_ids.html) and [identifiers.org](https://docs.identifiers.org/) for information about all the compact identifiers that are supported. You can choose to use an existing compact identifier provider for your DRS server, as we did in the example above using DOIs ("DRS Client Compact Identifier-Based URI Resolution Process - Existing Compact Identifier Provider"). Just keep in mind, each provider will have their own approach for generating compact identifiers and associating them with a DRS data object URL. Some compact identifier providers, like DOIs, provide a method whereby you can register in their network and get your own prefix, allowing you to mint your own accessions. Other services, like the University of California’s [EZID](https://ezid.cdlib.org/) service, provide accounts and a mechanism to mint accessions centrally for each of your data objects. For experimentation we recommend you take a look at the EZID website that allows you to create DOIs and ARKs and associate them with your data object URLs on your DRS server for testing purposes.
