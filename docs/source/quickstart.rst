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
