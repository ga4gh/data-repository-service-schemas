See the documentation on the [n2t.net](https://n2t.net/e/compact_ids.html) and [identifiers.org](https://docs.identifiers.org/) meta-resolvers for adding your own compact identifier type and registering your DRS server as a resolver. You can register new prefixes (or mirrors by adding resource provider codes) for free using a simple online form.

Keep in mind, while anyone can register prefixes, the identifiers.org/n2t.net sites do basic hand curation to verify new prefix and resource (provider code) requests. See those sites for more details on their security practices. For more information see

Starting with the prefix for our new compact identifier, let’s register the namespace `mydrsprefix` on identifiers.org/n2t.net and use 5-digit numeric IDs as our accessions. We will then link this to the DRS server at https://mydrs.server.org/ga4gh/drs/v1/ by filling in the provider details. Here’s what that the registration for our new namespace looks like on [identifiers.org](https://registry.identifiers.org/prefixregistrationrequest):

![Prefix Register 1](/data-repository-service-schemas/public/img/prefix_register_1.png)

![Prefix Register 2](/data-repository-service-schemas/public/img/prefix_register_2.png)
