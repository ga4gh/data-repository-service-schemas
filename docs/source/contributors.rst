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

You'll find the built documentation in ``docs/build/``.

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

Building documents
******************

To generate the OpenAPI 3 and SmartAPI descriptions, install
`swagger2openapi <https://github.com/Mermade/swagger2openapi>`_ then run::

    $ make schemas


Releases
--------

New versions are released when :py:data:`ga4gh.dos.__version__` is incremented,
a commit is tagged (either through a release or manually), and the tagged branch
builds successfully on Travis. When both conditions are met, Travis will 
`automatically upload <https://docs.travis-ci.com/user/deployment/pypi/>`_
the distribution to PyPI.

If :py:data:`ga4gh.dos.__version__` is not incremented in a new release, the
build may appear to complete successfully, but the package will not be uploaded
to PyPI as the distribution will be interpreted as a duplicate release and thus
refused.

The process above is currently managed by `david4096 <https://github.com/david4096>`_.
To transfer this responsibility, ownership of the PyPI package must be transferred
to a new account, and their details added to ``.travis.yml`` as described above.

Note that this repository will not become compliant with Semantic Versioning
until version 1.0 - until then, the API should be considered unstable.

Documentation is updated independently of this release cycle.

Code contributions
------------------

We welcome code contributions! Feel free to fork the repository and submit a
pull request. Please refer to this `contribution guide <https://github.com/ga4gh/ga4gh-schemas/blob/master/CONTRIBUTING.rst>`_
for guidance as to how you should submit changes.
