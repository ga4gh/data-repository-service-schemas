![ga4gh logo](http://genomicsandhealth.org/files/logo_ga.png)

Schemas for the Data Object Service (DOS) API
=============================================

This is used by the Data Working Group - Containers and Workflows Task Team

<img src="swagger_editor.png" width="48">[View in Swagger](http://editor.swagger.io/#/?import=https://raw.githubusercontent.com/ga4gh/data-object-schemas/feature/protobuf-bdo-2/swagger/proto/data_object.swagger.json)

The [Global Alliance for Genomics and Health](http://genomicsandhealth.org/) is an international
coalition, formed to enable the sharing of genomic and clinical data.

Containers and Workflows Task Team
----------------------------------

The [Data Working Group](http://ga4gh.org/#/) concentrates on data representation, storage, and analysis, including working with platform development partners and industry leaders to develop standards that will facilitate interoperability. The Containers & Workflows working group is an informal, multi-vendor working group focused on standards for exchanging Docker-based tools and CWL/WDL workflows, execution of Docker-based tools and workflows on clouds, and abstract access to cloud object stores.

What is DOS?
------------

Currently, this is the home of the Data Object Service (DOS) API proposal. This repo has a CWL-based build process ready to go and a place for us to collectively work on [USECASES.md](USECASES.md)

Key features of the current API proposal:

* TBD

Outstanding questions:

* TBD

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

    mv data_object.swagger.json swagger/proto/

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
