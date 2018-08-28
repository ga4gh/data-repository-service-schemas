# -*- coding: utf-8 -*-
import functools
import json
import logging
import time
import unittest
try:
    import urllib.parse as urllib  # For Python 3 compat
except ImportError:
    import urllib
import uuid

import ga4gh.dos.schema

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def test_requires(*operations):
    """
    This is a decorator that identifies what DOS operations a given test
    case uses (where each DOS operation is named by its `operationId` in
    the schema, e.g. ListDataBundles, UpdateDataObject, GetServiceInfo,
    etc.) and skips them if the operation is not supported by the
    implementation under test.

    For example, given this test setup::

        class Test(AbstractComplianceTest):
            supports = ['UpdateDataBundles']

            @test_requires('UpdateDataBundles')
            def test_update_data_bundles(self):
                self.dos_request('PUT', '/databundles/1234')

            @test_requires('ListDataBundles', 'UpdateDataBundles')
            def test_list_and_update_data_bundles(self):
                self.dos_request('GET', '/databundles')
                self.dos_request('PUT', '/databundles/1234')

    ``test_update_data_bundles`` would run and ``test_list_and_update_data_bundles``
    would be skipped.

    :param str \*operations: the operations supported by the decorated
                             test case
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self):
            unsupported = [op for op in operations if op not in self.supports]
            if unsupported:
                raise unittest.SkipTest("not supported: " + ", ".join(unsupported))
            return func(self)
        return wrapper
    return decorator


class AbstractComplianceTest(unittest.TestCase):
    """
    This class implements a number of compliance tests for Data Object Service
    implementations. It is meant to provide a single, standardized test
    harness to verify that a given DOS implementation acts in a manner
    consistent with the schema.

    Using the test harness is pretty straightforward, and only requires
    implementing a method that can make requests to the service under test
    (:meth:`~AbstractComplianceTest._make_request`). As this class subclasses
    :class:`unittest.TestCase`, all the functions exposed to a subclass
    of :class:`unittest.TestCase` (e.g. :meth:`~unittest.TestCase.setUpClass`)
    are available for use.

    This test suite does not perform any authentication testing. Requests made
    during testing are made with the assumption that they will be properly
    authenticated in :meth:`_make_request` or similar.

    For a service built using Chalice, you would likely be able to write
    something similar to this::

        from ga4gh.dos.test.compliance import AbstractComplianceTest
        from chalice import LocalGateway, Config
        from my_chalice_app import chalice_app

        class TestApp(AbstractComplianceTest):
            @classmethod
            def setUpClass(cls):
                cls.lg = LocalGateway(chalice_app, Config())

            def _make_request(self, meth, path, headers=None, body=None)
                headers = headers or {}
                r = self.lg.handle_request(method=meth, path='/ga4gh/dos/v1' + path,
                                           headers=headers, body=body)
                return r['body'], r['statusCode']

    You would then be able to run the compliance test suite however you
    normally run your tests (e.g. ``nosetests`` or ``python -m unittest discover``).

    :var supports: a list of supported DOS implementations. By default, this is
                   the list of all DOS operations, named by the `operationId`
                   key in the schema::

                       supports = ['GetServiceInfo', 'GetDataBundleVersions',
                                   'CreateDataBundle', 'ListDataBundles',
                                   'UpdateDataObject', 'GetDataObject', ...]

                    Adding / removing operations from this list will adjust
                    which tests are run. So, doing something like::

                        class Test(AbstractComplianceTest):
                            self.supports = ['ListDataObjects']

                    would skip all tests calling UpdateDataBundle, GetDataBundle,
                    and any other endpoint that is not ListDataObjects.
    """
    # Populate :var:`supports` with the `operationId` of each DOS endpoint
    # specified in the schema.
    supports = []
    for path in ga4gh.dos.schema.present_schema()['paths'].values():
        for method in path.values():
            supports.append(method['operationId'])

    def _make_request(self, meth, path, headers=None, body=None):
        """
        Method that makes requests to a DOS implementation under test
        given a method, path, request headers, and a request body.

        The provided path is the path provided in the Data Object Service
        schema - this means that in your implementation of this method,
        you might need to prepend the provided path with your ``basePath``,
        e.g. ``/ga4gh/dos/v1``.

        This method should return a tuple of the raw request content as a
        string and the return code of the request as an int.

        :param str meth: the HTTP method to use in the request (i.e. GET,
                         PUT, etc.)
        :param str path: path to make a request to, sans hostname (e.g.
                         `/databundles`)
        :param dict headers: headers to include with the request
        :param dict body: data to be included in the request body (serialized
                          as JSON)
        :rtype: tuple
        :returns: a tuple of the response body as a JSON-formatted string and the
                  response code as an int
        """
        raise NotImplementedError

    def dos_request(self, meth, path, headers={}, body=None, expected_status=200):
        """
        Wrapper function around :meth:`AbstractComplianceTest._make_request`.
        Logs the request being made, makes the request with
        :meth:`._make_request`, checks for errors, and performs transparent
        JSON de/serialization.

        It is assumed that any request made through this function is a
        request made to the underlying DOS implementation - e.g.,
        ``self.dos_request('https://example.com/')`` should be expected
        to fail.

        :param str meth: the HTTP method to use in the request (i.e. GET,
                         PUT, etc.)
        :param str path: path to make a request to, sans hostname (e.g.
                         `/databundles`)
        :param dict headers: headers to include with the request
        :param dict body: data to be included in the request body
                          (**not** serialized as JSON)
        :param int expected_status: expected HTTP status code. If the status
                                    code is not expected, an error will be
                                    raised.
        :rtype: dict
        :returns: the response body
        """
        # Log the request being made, make the request itself, then log the response.
        logger.debug("%s %s", meth, path)
        request, status = self._make_request(meth=meth, path=path, headers=headers,
                                             body=json.dumps(body))
        logger.info("{meth} {path} [{status}]".format(**locals()))

        # Check to make sure the return code is what we expect
        msg = "{meth} {path} returned {status}, expected {expected_status}: {request}"
        self.assertEqual(status, expected_status, msg=msg.format(**locals()))

        # Return the deserialized request body
        return json.loads(request)

    @staticmethod
    def get_query_url(path, **kwargs):
        """
        Returns the given path with the provided kwargs concatenated as
        query parameters, e.g.::

            >>> self.get_query_url('/dataobjects', alias=123)
            '/dataobjects?alias=123'

        :param str path: URL path without query parameters
        :param kwargs: query parameters
        :rtype: str
        """
        return path + '?' + urllib.urlencode(kwargs)

    @test_requires('ListDataObjects')
    def test_list_data_objects_simple(self):
        """Smoke test to verify that `GET /dataobjects` returns a response."""
        r = self.dos_request('GET', '/dataobjects')
        self.assertTrue(r)

    @test_requires('ListDataObjects', 'GetDataObject')
    def test_get_data_object(self):
        """
        Lists Data Objects and then gets one by ID.
        """
        # List all the data objects so we can pick one to test.
        r = self.dos_request('GET', '/dataobjects')
        data_object_1 = r['data_objects'][0]
        r = self.dos_request('GET', '/dataobjects/' + data_object_1['id'])
        data_object_2 = r['data_object']
        self.assertEqual(data_object_1, data_object_2)

    @test_requires('ListDataBundles', 'GetDataBundle')
    def test_get_data_bundle(self):
        """
        Lists data bundles and then gets one by ID.
        """
        # List all the data objects so we can pick one to test.
        r = self.dos_request('GET', '/databundles')
        data_bundle_1 = r['data_bundles'][0]
        r = self.dos_request('GET', '/databundles/' + data_bundle_1['id'])
        data_bundle_2 = r['data_bundle']
        self.assertEqual(data_bundle_1, data_bundle_2)

    @test_requires('GetDataBundle')
    def test_get_nonexistent_data_bundle(self):
        """
        Verifies that requesting a data bundle that doesn't exist results in HTTP 404
        """
        self.dos_request('GET', '/databundles/NonexistentDataBundle',
                         expected_status=404)

    @test_requires('UpdateDataObject')
    def test_update_nonexistent_data_object(self):
        """
        Verifies that trying to update a data object that doesn't exist
        returns HTTP 404
        """
        self.dos_request(meth='PUT', expected_status=404,
                         path='/dataobjects/NonexistentObjID')

    @test_requires('GetDataObject', 'ListDataObjects')
    def test_update_data_object_with_bad_request(self):
        """
        Verifies that attempting to update a data object with a malformed
        request returns HTTP 400
        """
        data_obj = self.dos_request('GET', '/dataobjects')['data_objects'][1]
        self.dos_request(meth='PUT', expected_status=400,
                         path='/dataobjects/' + data_obj['id'])

    @test_requires('ListDataObjects')
    def test_paging(self):
        """
        Demonstrates basic paging features.
        """
        # Make a request that will return more than one data object
        r = self.dos_request('GET', '/dataobjects')
        self.assertTrue(len(r['data_objects']) > 1)

        # Now that we have a request that we know will return more than
        # one data object, we can test and see if we can use paging to
        # return only one of those objects.
        r = self.dos_request('GET', self.get_query_url('/dataobjects', page_size=1))
        self.assertEqual(len(r['data_objects']), 1)
        self.assertEqual(r['next_page_token'], '1')

        # Test that page tokens work.
        r = self.dos_request('GET', self.get_query_url('/dataobjects',
                                                       page_size=1, page_token=1))
        self.assertEqual(len(r['data_objects']), 1)

    @test_requires('ListDataObjects')
    def test_nonexist_alias(self):
        """
        Test to ensure that looking up a nonexistent alias returns an
        empty list.
        """
        alias = str(uuid.uuid1())
        body = self.dos_request('GET', self.get_query_url('/dataobjects', alias=alias))
        self.assertEqual(len(body['data_objects']), 0)
        body = self.dos_request('GET', self.get_query_url('/databundles', alias=alias))
        self.assertEqual(len(body['data_bundles']), 0)

    @test_requires('ListDataObjects', 'UpdateDataObject', 'GetDataObject')
    def test_alias_update(self):
        """
        Demonstrates updating a data object with a given alias.
        """
        alias = 'daltest:' + str(uuid.uuid1())
        # First, select a "random" object that we can test
        body = self.dos_request('GET', '/dataobjects')
        data_object = body['data_objects'][9]
        url = '/dataobjects/' + data_object['id']

        # Try and update with no changes.
        self.dos_request('PUT', url, body={'data_object': data_object},
                         headers={'Content-Type': 'application/json'})
        # We specify the Content-Type since Chalice looks for it when
        # deserializing the request body server-side

        # Test adding an alias (acceptably unique to try
        # retrieving the object by the alias)
        data_object['aliases'].append(alias)

        # Try and update, this time with a change.
        update_response = self.dos_request('PUT', url, body={'data_object': data_object},
                                           headers={'Content-Type': 'application/json'})
        self.assertEqual(data_object['id'], update_response['data_object_id'])

        time.sleep(2)

        # Test and see if the update took place by retrieving the object
        # and checking its aliases
        get_response = self.dos_request('GET', url)
        self.assertEqual(update_response['data_object_id'], get_response['data_object']['id'])
        self.assertIn(alias, get_response['data_object']['aliases'])

        # Testing the update again by using a DOS ListDataObjectsRequest
        # to locate the object by its new alias.
        list_request = {
            'alias': alias,
            # We know the alias is unique, so even though page_size > 1
            # we expect only one result.
            'page_size': 10
        }
        list_url = self.get_query_url('/dataobjects', **list_request)
        list_response = self.dos_request('GET', list_url)
        self.assertEqual(1, len(list_response['data_objects']))
        self.assertIn(alias, list_response['data_objects'][0]['aliases'])

        # # Tear down and remove the test alias
        # params['body']['data_object']['aliases'].remove(alias)
        # self.dos_request('PUT', url, **params)

    @test_requires('ListDataObjects', 'UpdateDataObject')
    def test_full_data_object_update(self):
        """
        Demonstrates updating multiple fields of a data object at once.
        This incidentally also tests object conversion.
        """
        # First, select a "random" object that we can test
        body = self.dos_request('GET', '/dataobjects')
        data_object = body['data_objects'][6]
        url = '/dataobjects/' + data_object['id']

        # Make a new data object that is different from the data object we retrieved
        attributes = {
            # 'name' and 'description' are optional fields and might not be present
            'name': data_object.get('name', '') + 'test-suffix',
            # See DataBiosphere/dos-azul-lambda#87
            # 'description': data_object.get('description', '') + 'Change This',
            'urls': [
                {'url': 'https://cgl.genomics.ucsc.edu/'},
                {'url': 'https://github.com/DataBiosphere'}
            ]
        }
        data_object.update(attributes)

        # Now update the old data object with the new attributes we added
        self.dos_request('PUT', url, body={'data_object': data_object},
                         headers={'Content-Type': 'application/json'})
        time.sleep(2)  # Give the server some time to catch up

        # Test and see if the update took place
        get_response = self.dos_request('GET', url)
        self.assertEqual(get_response['data_object'], data_object)
