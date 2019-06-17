.. highlight:: python

Tools for DOS Implementations
=============================

The :mod:`ga4gh.dos` package contains some utilities that can help you
develop a compliant DOS resolver.

Dynamic ``/swagger.json`` with Chalice
--------------------------------------

If you're using Chalice, you can expose a subset of the Data Object Service
schema using :func:`ga4gh.dos.schema.from_chalice_routes`::

    from chalice import Chalice
    app = Chalice(...)

    @app.route('/swagger.json')
    def swagger():
        return ga4gh.dos.schema.from_chalice_routes(app.routes)

With the above code, a GET request to ``/swagger.json`` will return a schema
in the Swagger / OpenAPI 2 format that correctly lists only the endpoints that
are exposed by your app.

If you have a different ``basePath``, you can also specify that::

    @app.route('/swagger.json')
    def swagger():
        return ga4gh.dos.schema.from_chalice_routes(app.routes, base_path='/api')

Compliance testing
------------------

This package contains a testing suite
(:class:`~ga4gh.dos.test.integration.AbstractComplianceTest`)
that streamlines testing implementations of the Data Object Service
for compliance with the DOS schema.

This test suite is meant to supplement, and not replace, an existing
test suite. It does not:

* test authentication
* test health of the service(s) underpinning an implementation
* test any endpoints not defined in the Data Object Service schema

.. autoclass:: ga4gh.dos.test.compliance.AbstractComplianceTest
   :members: _make_request
