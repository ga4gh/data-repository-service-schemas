<img src="https://www.ga4gh.org/wp-content/themes/ga4gh-theme/gfx/GA-logo-horizontal-tag-RGB.svg" alt="GA4GH Logo" style="width: 400px;"/>

# Data Repository Service (DRS) API

<sup>`develop` branch status: </sup>[![Build Status](https://travis-ci.org/ga4gh/data-repository-service-schemas.svg?branch=develop)](https://travis-ci.org/ga4gh/data-repository-service-schemas?branch=develop)
<a href="https://ga4gh.github.io/data-repository-service-schemas/preview/develop/swagger.yaml"><img src="http://online.swagger.io/validator?url=https://ga4gh.github.io/data-repository-service-schemas/preview/develop/swagger.yaml" alt="Swagger Validator" height="20em" width="72em"></A> [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1405753.svg)](https://doi.org/10.5281/zenodo.1405753)

The [Global Alliance for Genomics and Health](http://genomicsandhealth.org/) (GA4GH) is an international coalition, formed to enable the sharing of genomic and clinical data.

# About the GA4GH Cloud Work Stream

The GA4GH [Cloud Work Stream](http://ga4gh.cloud) helps the genomics and health communities take full advantage of modern cloud environments.
Our initial focus is on “bringing the algorithms to the data”, by creating standards for defining, sharing, and executing portable workflows.

We work with platform development partners and industry leaders to develop standards that will facilitate interoperability.

# What is DRS?

The Data Repository Service (DRS) API provides a generic interface to data repositories so data consumers, including workflow systems, can access data in a single, standardized way regardless of where it’s stored or how it’s managed.
The primary functionality of DRS is to map a logical ID to a means for physically retrieving the data represented by the ID.

For more information see our HTML documentation links in the table below.

# API Definition

|  **Branch** | **Reference Documentation** | Swagger Editor |
| --- | --- | --- |
| **develop**: the stable development branch, into which feature branches are merged | [HTML](https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/) | [Swagger Editor](https://editor.swagger.io?url=https://ga4gh.github.io/data-repository-service-schemas/preview/develop/openapi.yaml) |
| **release 1.2.0**: The 1.2.0 release of DRS adds the standardized `/service-info` endpoint, and 2 `POST` endpoints that are functionally equivalent to the current `GET` endpoints, but they enable the submission of large passport tokens in the request body. | [HTML](https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.2.0/docs/) | [Swagger Editor](https://editor.swagger.io?url=https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.2.0/openapi.yaml) |
| **release 1.1.0**: The 1.1.0 release of DRS that includes *no* API changes only documentation changes. This introduces a new URI convention using compact identifiers along with clear directions on how to use identifiers.org/n2t.net to resolve them. | [HTML](https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.1.0/docs/) | [Swagger Editor](https://editor.swagger.io?url=https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.1.0/swagger.yaml) |
| **release 1.0.0**: The 1.0.0 release of DRS that is now an approved GA4GH standard | [HTML](https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.0.0/docs/) | [Swagger Editor](https://editor.swagger.io?url=https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-1.0.0/swagger.yaml) |
| **release 0.1**: Simplifying DRS to core functionality | [HTML](https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-0.1.0/docs/) | [Swagger Editor](https://editor.swagger.io?url=https://ga4gh.github.io/data-repository-service-schemas/preview/release/drs-0.1.0/swagger.yaml) |
| **release 0.0.1**: The initial DRS after the rename from DOS | [HTML](https://ga4gh.github.io/data-repository-service-schemas/preview/release/0.0.1/docs/) | [Swagger Editor](https://editor.swagger.io?url=https://ga4gh.github.io/data-repository-service-schemas/preview/release/0.0.1/swagger.yaml) |

To monitor development work on various branches, add 'preview/\<branch-name\>' to the master URLs above (e.g., 'https://ga4gh.github.io/data-repository-service-schemas/preview/\<branch-name\>/docs').

# How to Contribute Changes

See [CONTRIBUTING.md](CONTRIBUTING.md).

If a security issue is identified with the specification, please send an email to security-notification@ga4gh.org detailing your concerns.

# License

See the [LICENSE](LICENSE).

# More Information

* [Global Alliance for Genomics and Health](http://genomicsandhealth.org)
* [GA4GH Cloud Work Stream](http://ga4gh.cloud)
