.. highlight:: console

Contributor's Guide
===================

Installing
----------

To install for development, install from source (and be sure to install the
development requirements as well)::

    $ git clone https://github.com/ga4gh/data-object-service-schemas.git
    $ cd data-object-service-schemas
    $ python setup.py develop
    $ pip install -r requirements.txt

Documentation
-------------

We use Sphinx for our documentation. You can generate an HTML build like so::

    $ cd docs/
    $ make html

You'll find the built documentation in `docs/build/`.

Tests
-----

To run tests::

    $ nosetests python/

The Travis test suite also tests for PEP8 compliance (checking for all errors
except line length)::

    $ flake8 --select=E121,E123,E126,E226,E24,E704,W503,W504 --ignore=E501 python/

Schema architecture
-------------------

The canonical, authoritative schema is located at ``openapi/data_object_service.swagger.yaml``. All schema changes
must be made to the Swagger schema, and all other specifications (e.g. SmartAPI, OpenAPI 3) are derived from it.

Code contributions
------------------

We welcome code contributions! Feel free to fork the repository and submit a
pull request. Please refer to this `contribution guide <https://github.com/ga4gh/ga4gh-schemas/blob/master/CONTRIBUTING.rst>`_
for guidance as to how you should submit changes.

