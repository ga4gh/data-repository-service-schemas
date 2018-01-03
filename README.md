<img src="https://www.ga4gh.org/gfx/GA-logo-horizontal-tag-RGB.svg" alt="Drawing" style="width: 120px;" alt="GA4GH colored ring logo"/>

![travis status](https://travis-ci.org/ga4gh/data-object-schemas.svg?branch=master)


Schemas for the Data Object Service (DOS) API
=============================================

[View the schemas in Swagger UI](http://ga4gh.github.io/data-object-schemas)

The [Global Alliance for Genomics and Health](http://genomicsandhealth.org/) is an international
coalition, formed to enable the sharing of genomic and clinical data. This collaborative consortium
takes place primarily via github and public meetings. Join the issues today to help us make
a cloud agnostic Data Object Service!

Cloud Workstream
----------------

The [Data Working Group](http://ga4gh.org/#/) concentrates on data representation, storage, and analysis,
including working with platform development partners and industry leaders to develop standards that will
facilitate interoperability. The Cloud Workstream is an informal, multi-vendor working group focused on
standards for exchanging Docker-based tools and CWL/WDL workflows, execution of Docker-based tools and
workflows on clouds, and abstract access to cloud object stores.

What is DOS?
------------

Currently, this is the home of the Data Object Service (DOS) API proposal. This repo has a CWL-based
build process ready to go and a place for us to collectively work on [USECASES.md](USECASES.md).

This proposal for a DOS release is based on the schema work of Brian W. and others from OHSU along
with work by UCSC.  It also is informed by existing object storage systems such as:

* GNOS: http://annaisystems.com/ (as used by PCAWG, see https://pcawg.icgc.org)
* ICGC Storage: as used to store data on S3, see https://github.com/icgc-dcc/dcc-storage and https://dcc.icgc.org/icgc-in-the-cloud/aws
* HCA Storage: see https://dss.staging.data.humancellatlas.org/ and https://github.com/HumanCellAtlas/data-store
* the GDC Storage: see https://gdc.cancer.gov
* Keep by Curoverse: see https://arvados.org/ and https://github.com/curoverse/arvados

The goal of DOS is to create a generic API on top of these and other projects, so workflow systems can
access data in the same way regardless of project.  One section of the API focuses on how to read and
write data objects to cloud environments and how to join them together as data bundles (Data object management).
 Another focuses on the ability to find data objects across cloud environments and implementations of DOS
 (Data object queries).  The latter is likely to be worked on in conjunction with the GA4GH Discovery Workstream.

Key features of the current API proposal:

#### Data object management

This section of the API focuses on how to read and write data objects to cloud environments
and how to join them together as data bundles.  Data bundles are simply a flat collection
of one or more files.  This section of the API enables:

* create/update/delete a file
* create/update/delete a data bundle
* register UUIDs with these entities (an optionally track versions of each)
* generate signed URLs and/or cloud specific object storage paths and temporary credentials

#### Data object queries

A key feature of this API beyond creating/modifying/deletion files is the ability to
find data objects across cloud environments and implementations of DOS.  This
section of the API allows users to query by data bundle or file UUIDs which returns
information about where these data objects are available.  This response will
typically be used to find the same file or data bundle located across multiple
cloud environments.

Building the client and server
------------------------------

You can use `pip` to install a python client and server that implements these schemas.

```
virtualenv env
source env/bin/activate
pip install git+git://github.com/ga4gh/data-object-schemas@master --process-dependency-links
```

This will add the python modules `ga4gh.dos.server` and `ga4gh.dos.client` you can use in
your projects.

There is also a CLI hook.

```
ga4gh_dos_server
# In another terminal
ga4gh_dos_demo
```


Building Documents
------------------

Make sure you have Docker installed for your platform and the `cwltool`.

    virtualenv env
    source env/bin/activate
    pip install -r python/dev-requirements.txt

You can generate the [Swagger](http://swagger.io/) YAML from the Protocol Buffers:

    cwltool CWLFile

Find the output in `data_objects_service.swagger.json` and this can be loaded in the [Swagger editor](http://swagger.io/swagger-editor/).  Use the GitHub raw feature to generate a URL you can load.

When you're happy with the changes, checkin this file:

    mv data_objects_service.swagger.json swagger/proto/

And commit your changes, pushing to the appropriate branch.


Roadmap
-------

## Goal

Create an interoperability layer that allows metadata about resources to be interchanged using a common client.

## Metrics of success

What data are available by DOS? GDC? TOPMed? HCA? How many files/bundles/PB?

How many workflows have been converted to use DOS downloader?

How many applications or services offer a DOS interop layer?

## Milestones

### Stable schematization

* Bring the schemas repository to a stable state.
* Demonstrate usage of the schemas in clients and servers.
* Make the schematization easily available to other software.

### Lambda Interoperability Layer

* Create an interop layer for:
	* DSS
	* indexd
* Demonstrate authentication/authorization handling.

### Supporting software

* Create a DOS downloader that can handle resources in third party APIs.
* Demonstrate usage with Kafka/ES for DOS-connect.
* Create a "best practices" description of creating an HTTP-signing DOS endpoint.
* Demonstrate a DOS endpoint indexer, which will provide more flexible metadata queries.

### Workflows and Visualization

* Extend a workflow to use the DOS downloader (as opposed to a single URL).
* Create a basic workflow stage that can be reused to extend other workflows to use DOS downloader.
* Create a basic single page app  for viewing the contents of a DOS registry.

## Timeline

### December 2017

We are currently most of the way through *Stabilizing Schemas* and headed into *Lambda Interoperability Layer*.

### January 2017

We are deep into *Lambda Interoperability Layer* demonstrating working tests against real data served by GDC.

Some work towards demonstrating authentication will be offered for this lambda.

### February 2017

The lambda for signpost should have fleshed out all interop concerns. Work should focus on DSS lambda.

Some work has been shown on the DOS downloader.

Some software for syndication/replication is demonstrated (DOS-connect).

### March 2017

DOS lambdas are available for use for accessing data as a beta. Lambda deployment follows common SDLC practices (alpha, beta). Some metrics are added. 

Data in DOS endpoints has been indexed and made available for more complicated queries as a demonstration.

### April 2017

Practical authentication systems are combined with URL signing features in alpha.

A demonstration workflow uses DOS to download data.

### May 2017

The DOS downloader is extended to support other resources types. Published to PyPi.

Authentication schemes that require exchanging of third party API keys are demonstrated.

### June 2017

Publish a workflow stage that can be easily reused to access data using the DOS downloader.

Demonstrate API integration with metadata indexes to analyze "findability" of data.

### July 2017

Integration with a single page webapp allows for DOS manifests to be realized as files by the DOS downloader.

How to contribute changes
-------------------------

Take cues for now from the [ga4gh/schemas](https://github.com/ga4gh/schemas/blob/master/CONTRIBUTING.rst) document.

License
-------

See the [LICENSE]

More Information
----------------

* [Global Alliance for Genomics and Health](http://genomicsandhealth.org)
* [Google Forum](https://groups.google.com/forum/#!forum/ga4gh-dwg-containers-workflows)
