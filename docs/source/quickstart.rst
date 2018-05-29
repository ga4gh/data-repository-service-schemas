.. highlight:: console

Quickstart
==========

Installing
----------

Installing is quick and easy. First, it's always good practice to
work in a virtualenv::

    $ virtualenv venv
    $ source venv/bin/activate

Then, install from PyPI::

    $ pip install ga4gh-dos-schemas

Or, to install from source::

    $ git clone https://github.com/ga4gh/data-object-service-schemas.git
    $ cd data-object-service-schemas
    $ python setup.py install

Running the client and server
-----------------------------

There's a handy command line hook for the server::

    $ ga4gh_dos_server

and for the client::

    $ ga4gh_dos_demo

Building documents
------------------

The schemas are editable as OpenAPI 2 YAML files. To generate OpenAPI 3
descriptions install `swagger2openapi <https://github.com/Mermade/swagger2openapi>`_
and run the following::

    $ swagger2openapi -y openapi/data_object_service.swagger.yaml > openapi/data_object_service.openapi.yaml
