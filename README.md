[![GA4GH Logo](https://www.ga4gh.org/gfx/GA-logo-horizontal-tag-RGB.svg" style="width: 120px;" alt="GA4GH colored ring logo)](https://www.ga4gh.org/)
[![Build Status](https://travis-ci.org/ga4gh/data-object-service-schemas.svg?branch=master)](https://travis-ci.org/ga4gh/data-object-service-schemas)
[![Swagger Validator](https://img.shields.io/swagger/valid/2.0/https/raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v2.0/json/petstore-expanded.json.svg)](https://raw.githubusercontent.com/ga4gh/data-object-service-schemas/master/openapi/data_object_service.swagger.yaml)

# Schemas for the Data Object Service (DOS) API

[View the schemas in Swagger UI](http://ga4gh.github.io/data-object-service-schemas)

The goal of DOS is to create a generic API on top of existing object storage systems
so workflow systems can access data in a single, standard way regardless of where it's
stored. It's maintained by the [GA4GH Data Working Group](https://www.ga4gh.org).

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

For more on getting started, check out the [quickstart guide](docs/source/quickstart.rst).
For everything else, including API documentation and project background, refer to our
[ReadTheDocs](https://example.com) site.
