![ga4gh logo](http://genomicsandhealth.org/files/logo_ga.png)

Schemas for the Data Object API
======================================

This is used by the Data Working Group - Containers and Workflows Task Team

<img src="swagger_editor.png" width="48">[View in Swagger](http://editor.swagger.io/#/?import=https://raw.githubusercontent.com/ga4gh/data-object-schemas/develop/swagger/proto/workflow_execution.swagger.json)

The [Global Alliance for Genomics and Health](http://genomicsandhealth.org/) is an international
coalition, formed to enable the sharing of genomic and clinical data.

The [Data Working Group](http://ga4gh.org/#/) concentrates on data representation, storage,
and analysis, including working with platform development partners and
industry leaders to develop standards that will facilitate
interoperability.

Containers and Workflows Task Team
----------------------------------

The Containers & Workflows working group is an informal, multi-vendor working group born out of the BOSC 2014 codefest, consisting of various organizations and individuals that have an interest in portability of data analysis workflows. Our goal is to create specifications that enable data scientists to describe analysis tools and workflows that are powerful, easy to use, portable, and support reproducibility for a variety of problem areas including data-intensive science like bioinformatics, physics, and astronomy; and business analytics such as log analysis, data mining, and ETL.

From within this group, two approaches have emerged, resulting in the production of two distinct but complementary specifications: the Common Workflow Language, or CWL, and the Workflow Description Language, or WDL. The CWL approach emphasizes execution features and machine-readability, and serves a core target audience of software and platform developers. The WDL approach, on the other hand, emphasizes scripting  and human-readability, and serves a core target audience of research scientists.

Together, these two specifications cover a very wide spectrum of analysis use cases. Work is underway to ensure interoperability through conversion and related utilities.

What is this?
------------

Currently, this is the home of the Data Object API proposal. This is just the initial checkin based on the WES repo so we have a build process ready to go.  We need to work on the schema next.

Key features of the current API proposal:

* TBD

Outstanding questions:

* TBD

How to view
------------

See the swagger editor to view our [schema in progress](http://editor.swagger.io/#/?import=https://raw.githubusercontent.com/ga4gh/data-object-schemas/develop/src/main/resources/swagger/ga4gh-tool-discovery.yaml).

If the current schema fails to validate, visit [debugging](http://online.swagger.io/validator/debug?url=https://raw.githubusercontent.com/ga4gh/data-object-schemas/develop/src/main/resources/swagger/ga4gh-tool-discovery.yaml)

Building Documents
------------------

Make sure you have Docker installed for your platform and the `cwltool`.

    virtualenv env
    source env/bin/activate
    pip install setuptools==28.8.0
    pip install cwl-runner cwltool==1.0.20161114152756 schema-salad==1.18.20161005190847 avro==1.8.1

You can generate the [Swagger](http://swagger.io/) YAML from the Protocol Buffers:

    cwltool CWLFile

Find the output in `workflow_execution.swagger.json` and this can be loaded in the [Swagger editor](http://swagger.io/swagger-editor/).  Use the GitHub raw feature to generate a URL you can load.

When you're happy with the changes, checkin this file:

    mv workflow_execution.swagger.json swagger/proto/

And commit your changes.

How to contribute changes
-------------------------

Take cues for now from the [ga4gh/schemas](https://github.com/ga4gh/schemas/blob/master/CONTRIBUTING.rst) document.

License
-------

See the [LICENSE]

  []: http://genomicsandhealth.org/files/logo_ga.png
  [Global Alliance for Genomics and Health]: http://genomicsandhealth.org/
  [INSTALL.md]: INSTALL.md
  [CONTRIBUTING.md]: CONTRIBUTING.md
  [LICENSE]: LICENSE
  [Google Forum]: https://groups.google.com/forum/#!forum/ga4gh-dwg-containers-workflows
