<img src="https://www.ga4gh.org/wp-content/themes/ga4gh-theme/gfx/GA-logo-horizontal-tag-RGB.svg" alt="GA4GH Logo" style="width: 400px;"/>

# Data Repository Service (DRS) API

<sup>`develop` branch status: </sup>[![Build Status](https://travis-ci.org/ga4gh/data-repository-service-schemas.svg?branch=develop)](https://travis-ci.org/ga4gh/data-repository-service-schemas?branch=develop)
<a href="https://ga4gh.github.io/data-repository-service-schemas/preview/develop/swagger.yaml"><img src="http://online.swagger.io/validator?url=https://ga4gh.github.io/data-repository-service-schemas/preview/develop/swagger.yaml" alt="Swagger Validator" height="20em" width="72em"></A>
[![Read the Docs badge](https://readthedocs.org/projects/data-repository-service/badge/)](https://data-repository-service.readthedocs.io/en/latest)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ga4gh-drs-schemas.svg)

The [Global Alliance for Genomics and Health](http://genomicsandhealth.org/) (GA4GH) is an international coalition, formed to enable the sharing of genomic and clinical data.

# About the GA4GH Cloud Work Stream

The GA4GH [Cloud Work Stream](https://ga4gh.cloud) helps the genomics and health communities take full advantage of modern cloud environments.
Our initial focus is on “bringing the algorithms to the data”, by creating standards for defining, sharing, and executing portable workflows.

We work with platform development partners and industry leaders to develop standards that will facilitate interoperability.

# What is DRS?

The Data Repository Service (DRS) API provides a generic interface to data repositories so data consumers, including workflow systems, can access data in a single, standard way regardless of where it’s stored and how it’s managed.
The primary functionality of DRS is to map a logical ID to a means for physically retrieving the data represented by the ID.

# API Definition

|  **Branch** | **Reference Documentation** | **[OpenAPI YAML description](openapi/data_repository_service.swagger.yaml)** |
| --- | --- | --- |
| **master**: the current release | [HTML](https://ga4gh.github.io/data-repository-service-schemas/docs/) | [Swagger](https://ga4gh.github.io/data-repository-service-schemas/swagger-ui/) |
| **develop**: the stable development branch, into which feature branches are merged | [HTML](https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/) | [Swagger](https://ga4gh.github.io/data-repository-service-schemas/preview/develop/swagger-ui/) |
| **release 0.0.1**: the initial DRS after the rename from DOS | [HTML](https://ga4gh.github.io/data-repository-service-schemas/preview/release/0.0.1/docs/) | [Swagger](https://ga4gh.github.io/data-repository-service-schemas/preview/release/0.0.1/swagger-ui/) |
| **release 0.1**: the initial DRS after the rename from DOS | [HTML](https://ga4gh.github.io/data-repository-service-schemas/preview/release/0.1/docs/) | [Swagger](https://ga4gh.github.io/data-repository-service-schemas/preview/release/0.1/swagger-ui/) |

To monitor the latest development work on various branches, add 'preview/\<branch\>' to the master URLs above (e.g., 'https://ga4gh.github.io/workflow-execution-service/preview/\<branch\>/docs').

# Use Cases

See the [Use Cases](USECASES.md) document for DRS use cases and possible
future directions.

# How to Contribute Changes

See [CONTRIBUTING.md](CONTRIBUTING.md).

If a security issue is identified with the specification, please send an email to security-notification@ga4gh.org detailing your concerns.

# License

See the [LICENSE](LICENSE).

# More Information

* [Global Alliance for Genomics and Health](http://genomicsandhealth.org)
* [GA4GH Cloud Work Stream](https://ga4gh.cloud)
