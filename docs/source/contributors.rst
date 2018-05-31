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
    $ pip install -r dev-requirements.txt

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

The Travis test suite also tests for PEP8 compliance (with
`some exceptions <http://flake8.pycqa.org/en/latest/user/violations.html#ignoring-violations-with-flake8>`_)::

    $ flake8 python/

Code contributions
------------------

We welcome code contributions! Feel free to fork the repository and submit a
pull request. Please refer to this `contribution guide <https://github.com/ga4gh/ga4gh-schemas/blob/master/CONTRIBUTING.rst>`_
for guidance as to how you should submit changes.
