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

The goal of DRS is to create a generic API on top of existing object storage systems
so workflow systems can access data in a single, standard way regardless of where it's
stored. It's maintained by the [GA4GH Cloud Workstream](https://github.com/ga4gh/wiki/wiki).

## Key features

The API is split into two sections:

* **Data Object management**, which enables the creation, updating, deletion, versioning,
  and unique identification of files and data bundles (flat collections of files); and
* **Data Object querying**, which can locate data objects across different cloud environments
  and DRS implementations.

# API Definition

See the human-readable **Reference Documentation**  ([Released (master)](https://ga4gh.github.io/data-repository-service-schemas/docs/) and [Stable Development (develop)](https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/))
and the **[OpenAPI YAML description](openapi/data_repository_service.swagger.yaml)**. You can also explore the specification in the Swagger UI ([Released (master)](https://ga4gh.github.io/data-repository-service-schemas/swagger-ui/) and [Stable Development (develop)](https://ga4gh.github.io/data-repository-service-schemas/preview/develop/swagger-ui/)).

> All documentation and pages hosted at 'ga4gh.github.io/data-repository-service-schemas' reflect the latest API release from the `master` branch. To monitor the latest development work on various branches, add 'preview/\<branch\>' to the URLs above (e.g., 'https://ga4gh.github.io/workflow-execution-service/preview/\<branch\>/docs'). To view the latest *stable* development API specification, refer to the `develop` branch.

# Use Cases

See the [Use Cases](USECASES.md) document for DRS use cases and possible
future directions.

# Example DRS Server and Client

## Getting started

Installing is as easy as:

```
$ pip install ga4gh-dos-schemas
```

This will install both a demonstration server and a Python client that will allow you to
manage Data Objects in a local server.

## Sample Service

You can start the demo server using `ga4gh_drs_server`.
This starts a Data Repository Service at http://localhost:8080.

```
wget http://hgdownload.cse.ucsc.edu/goldenPath/hg38/chromosomes/chr22.fa.gz
md5sum chr22.fa.gz
# 41b47ce1cc21b558409c19b892e1c0d1  chr22.fa.gz
curl -X POST -H 'Content-Type: application/json' \
    --data '{"data_object":
              {"id": "hg38-chr22",
               "name": "Human Reference Chromosome 22",
               "checksums": [{"checksum": "41b47ce1cc21b558409c19b892e1c0d1", "type": "md5"}],
               "urls": [{"url": "http://hgdownload.cse.ucsc.edu/goldenPath/hg38/chromosomes/chr22.fa.gz"}],
               "size": "12255678"}}' http://localhost:8080/ga4gh/dos/v1/dataobjects
# We can then get the newly created Data Object by id
curl http://localhost:8080/ga4gh/dos/v1/dataobjects/hg38-chr22
# Or by checksum!
curl -X GET http://localhost:8080/ga4gh/dos/v1/dataobjects -d checksum=41b47ce1cc21b558409c19b892e1c0d1
```

## For More Information on the Sample Service and Client

For more on getting started, check out the
[quickstart guide](https://data-repository-service.readthedocs.io/en/latest/quickstart.html)
or the rest of the documentation at [ReadtheDocs](https://data-repository-service.readthedocs.io/en/latest/)!

# How to Contribute Changes

See [CONTRIBUTING.md](CONTRIBUTING.md).

If a security issue is identified with the specification, please send an email to security-notification@ga4gh.org detailing your concerns.

# License

See the [LICENSE](LICENSE).

# More Information

* [Global Alliance for Genomics and Health](http://genomicsandhealth.org)
* [GA4GH Cloud Work Stream](https://ga4gh.cloud)
