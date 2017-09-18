![ga4gh logo](http://genomicsandhealth.org/files/logo_ga.png)

Schemas for the Data Object Service (DOS) API
=============================================

This is used by the Data Working Group - Containers and Workflows Task Team

<img src="swagger_editor.png" width="48">[View in Swagger](http://editor2.swagger.io/#/?import=https://raw.githubusercontent.com/ga4gh/data-object-schemas/feature/protobuf-bdo-2/swagger/proto/data_objects.swagger.json)

The [Global Alliance for Genomics and Health](http://genomicsandhealth.org/) is an international
coalition, formed to enable the sharing of genomic and clinical data.

Containers and Workflows Task Team
----------------------------------

The [Data Working Group](http://ga4gh.org/#/) concentrates on data representation, storage, and analysis, including working with platform development partners and industry leaders to develop standards that will facilitate interoperability. The Containers & Workflows working group is an informal, multi-vendor working group focused on standards for exchanging Docker-based tools and CWL/WDL workflows, execution of Docker-based tools and workflows on clouds, and abstract access to cloud object stores.

What is DOS?
------------

Currently, this is the home of the Data Object Service (DOS) API proposal. This repo has a CWL-based build process ready to go and a place for us to collectively work on [USECASES.md](USECASES.md)

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

Building Documents
------------------

Make sure you have Docker installed for your platform and the `cwltool`.

    virtualenv env
    source env/bin/activate
    pip install setuptools==28.8.0
    pip install cwl-runner cwltool==1.0.20161114152756 schema-salad==1.18.20161005190847 avro==1.8.1

You can generate the [Swagger](http://swagger.io/) YAML from the Protocol Buffers:

    cwltool CWLFile

Find the output in `data_object.swagger.json` and this can be loaded in the [Swagger editor](http://swagger.io/swagger-editor/).  Use the GitHub raw feature to generate a URL you can load.

When you're happy with the changes, checkin this file:

    mv data_objects.swagger.json swagger/proto/

And commit your changes.

How to contribute changes
-------------------------

Take cues for now from the [ga4gh/schemas](https://github.com/ga4gh/schemas/blob/master/CONTRIBUTING.rst) document.

Submodule Magic
---------------

This is how I added a submodule for Brian Walsh's changes to the core schema:

    git submodule add https://github.com/ga4gh/ga4gh-schemas.git
    cd ga4gh-schemas
    git checkout data-objects
    cd ..
    git add ga4gh-schemas
    git commit -a -m 'adding in submodule dep for data-objects branch'
    git push

See this [article](https://stackoverflow.com/questions/1777854/git-submodules-specify-a-branch-tag) for info on this.

To update:

    cd ga4gh-schemas
    git pull
    git submodule update

License
-------

See the [LICENSE]

More Information
----------------

* [Global Alliance for Genomics and Health](http://genomicsandhealth.org)
* [Google Forum](https://groups.google.com/forum/#!forum/ga4gh-dwg-containers-workflows)


TODO/Questions
--------------
* Are data object ids supposed to be globally unique?  Could they be URIs instead of opaque UUIDs?
* can we move the schemas into this repo? Easier to release since won't be tied to GA4GH schemas release.
* do we want to use the [data bundles concept](https://docs.google.com/document/d/1d-9eu5X6ioOlqOJ9kkY8lHvXDF-KoynlmqJbuKVPMF0/edit#heading=h.b3jd47oqdd2e)? Often times we want to be able to model related files (like a workflow output) together in some way.  The data bundle concept supports this.
* do we want to support versioning (of files and data bundles)?  Implicit support right now in the sense that you can get an array of files or data bundles and use timestamp to understand their version.
* do we want to support provenance?  Brian W's schema has a provenance object.
* do we want to include bio-specific data in the API?  This is a bigger question of how generic do we want DOS to be.  I lean towards really generic and, therefore, all biospecimen metadata should just be in JSON files that are part of the data bundle.  The alternative is to include links to other GDC/GA4GH metadata structures as Brian W. has done here.  
    * related, do we want to offer search on the bio-specific data?
* do all the timestamps need to be generated server-side?  This might be key for supporting versioning.
* questions about Brian W's schema:
    * how does Brian W. link datasets and files?  I don't see a `dataset_id` in the `DataObject` message.
    * how does Brian W. search on keys?  What field is `has_keys` searching on for DataObjects?  How should we expose search for other entities in the DataObjects or DataBundleObjects?
* other fields from GDC to consider:
    * state
    * file_state
    * error_type
    * submitter_id
