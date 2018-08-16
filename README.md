# Schemas for the Data Object Service (DOS) API
<a href="https://ga4gh.org"><img src="https://www.ga4gh.org/gfx/GA-logo-horizontal-tag-RGB.svg" width="200" /></a><br />
[![Build Status](https://travis-ci.org/ga4gh/data-object-service-schemas.svg?branch=master)](https://travis-ci.org/ga4gh/data-object-service-schemas)
[![Swagger Validator](https://img.shields.io/swagger/valid/2.0/https/raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v2.0/json/petstore-expanded.json.svg)](https://raw.githubusercontent.com/ga4gh/data-object-service-schemas/master/openapi/data_object_service.swagger.yaml)
[![Read the Docs badge](https://readthedocs.org/projects/data-object-service/badge/)](https://data-object-service.readthedocs.io/en/latest)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ga4gh-dos-schemas.svg)

[View the schemas in Swagger UI](http://ga4gh.github.io/data-object-service-schemas)

The goal of DOS is to create a generic API on top of existing object storage systems
so workflow systems can access data in a single, standard way regardless of where it's
stored. It's maintained by the [GA4GH Cloud Workstream](https://github.com/ga4gh/wiki/wiki).

## Key features

The API is split into two sections:

* **data object management**, which enables the creation, updating, deletion, versioning,
  and unique identification of files and data bundles (flat collections of files); and
* **data object querying**, which can locate data objects across different cloud environments
  and DOS implementations.

## Getting started

Installing is as easy as:

```
$ pip install ga4gh-dos-schemas
```

This will install both a demonstration server and a Python client that will allow you to
manage Data Objects in a local server. You can start the demo server using `ga4gh_dos_server`.
This starts a Data Object Service at http://localhost:8080.

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

For more on getting started, check out the
[quickstart guide](https://data-object-service.readthedocs.io/en/latest/quickstart.html)
or the rest of the documentation at [ReadtheDocs](https://data-object-service.readthedocs.io/en/latest/)!

## Getting involved!

The Data Object Service Schemas are Apache 2 Licensed Open Source software. Please join us
in the [issues](https://github.com/ga4gh/data-object-service-schemas/issues) or check out the
contributing docs!
