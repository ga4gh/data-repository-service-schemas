# -*- coding: utf-8 -*-
import functools
import hashlib
import json
import logging
import random
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

            @classmethod
            def _make_request(self, meth, path, headers=None, body=None)
                headers = headers or {}
                r = self.lg.handle_request(method=meth, path='/ga4gh/dos/v1' + path,
                                           headers=headers, body=body)
                return r['body'], r['statusCode']

    You would then be able to run the compliance test suite however you
    normally run your tests (e.g. ``nosetests`` or ``python -m unittest discover``).

    :var supports: a list of supported DOS operations. By default, this is
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

    @classmethod
    def _make_request(cls, meth, path, headers=None, body=None):
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

    @classmethod
    def dos_request(cls, meth, path, headers=None, body=None, expected_status=200):
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
        # DOS only really speaks JSON, so we can assume that if data is being
        # sent with a request, that data will be JSON
        headers = headers or {}
        if body and 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
        request, status = cls._make_request(meth=meth, path=path, headers=headers,
                                            body=json.dumps(body))
        logger.info("{meth} {path} [{status}]".format(**locals()))

        # Check to make sure the return code is what we expect
        msg = "{meth} {path} returned {status}, expected {expected_status}: {request}"
        # We could use :meth:`assertEqual` here, but if we do,
        # :meth:`dos_request` must be an instance method. Since the only
        # advantage we really lose is a prettier error message, we can
        # be a little verbose this one time.
        # It's preferable that :meth:`dos_request` be defined as a class method
        # to allow one-time server setup to be performed in meth:`setUpClass`,
        # which must necessarily be a class method.
        if not status == expected_status:
            raise AssertionError(msg.format(**locals()))

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

    @staticmethod
    def generate_data_objects(amount):
        """
        Yields a specified number of data objects with random attributes.

        :param int amount: the amount of data objects to generate
        """
        for _ in range(amount):
            yield {
                'id': str(uuid.uuid1()),
                'name': str(uuid.uuid1()),
                'size': str(random.randint(2**0, 2**32)),
                'created': '2018-08-29T19:58:52.648Z',
                'updated': '2018-08-29T19:58:52.648Z',
                'version': str(uuid.uuid1()),
                'mime_type': 'application/json',
                'checksums': [{
                    'checksum': hashlib.md5(str(uuid.uuid1()).encode('utf-8')).hexdigest(),
                    'type': 'md5'
                }],
                'urls': [
                    {'url': str(uuid.uuid1())},
                    {'url': str(uuid.uuid1())}
                ],
                'description': str(uuid.uuid1()),
                'aliases': [str(uuid.uuid1())],
            }

    @staticmethod
    def generate_data_bundles(amount):
        """
        Yields a specified number of data bundles with random attributes.

        :param int amount: the amount of data bundles to generate
        """
        for bdl in AbstractComplianceTest.generate_data_objects(amount):
            del bdl['name']
            del bdl['size']
            del bdl['mime_type']
            del bdl['urls']
            bdl.update({'data_object_ids': [str(uuid.uuid1()), str(uuid.uuid1())]})
            yield bdl

    def get_random_data_object(self):
        """
        Retrieves a 'random' data object by performing a ListDataObjects
        request with a large page size then randomly selecting a data
        object from the response.

        As this test utilizes the ListDataObjects operation, be sure to
        specify that as a test requirement with :func:`test_requires`
        when using this context manager in a test case.

        Usage::

            obj, url = self.get_random_data_object()

        :returns: a random data object as a dict and its relative URL
                  (e.g. '/dataobjects/abcdefg-12345') as a string
        :rtype: tuple
        """
        r = self.dos_request('GET', self.get_query_url('/dataobjects', page_size=100))
        data_obj = random.choice(r['data_objects'])
        url = '/dataobjects/' + data_obj['id']
        return data_obj, url

    def get_random_data_bundle(self):
        """
        Retrieves a 'random' data bundle. Similar to :meth:`get_random_data_object`
        but retrieves a data bundle instead.
        """
        r = self.dos_request('GET', self.get_query_url('/databundles', page_size=100))
        data_bdl = random.choice(r['data_bundles'])
        url = '/databundles/' + data_bdl['id']
        return data_bdl, url

    # # ListDataObject tests
    @test_requires('ListDataObjects')
    def test_list_data_objects_simple(self):
        """
        Smoke test to verify that `GET /dataobjects` returns a response.
        """
        r = self.dos_request('GET', '/dataobjects')
        self.assertTrue(r)

    @test_requires('ListDataObjects')
    def test_list_data_objects_by_checksum(self):
        """
        Test that filtering by checksum in ListDataObjects works nicely.
        Since we can assume that checksums are unique between data
        objects, we can test this functionality by selecting a random
        data object then using ListDataObjects with a checksum parameter
        and asserting that only one result is returned and that the
        result returned is the same as the one queried.
        """
        obj, _ = self.get_random_data_object()
        for cs in obj['checksums']:
            url = self.get_query_url('/dataobjects', checksum=cs['checksum'], checksum_type=cs['type'])
            r = self.dos_request('GET', url)
            self.assertEqual(len(r['data_objects']), 1)
            self.assertEqual(r['data_objects'][0]['id'], obj['id'])

    @test_requires('ListDataObjects')
    def test_list_data_objects_by_alias(self):
        """
        Tests that filtering by alias in ListDataObjects works. We do
        this by selecting a random data object with ListDataObjects
        then performing another ListDataObjects query but filtering
        by the alias, then checking that every returned object contains
        the proper aliases.
        """
        reference_obj, _ = self.get_random_data_object()
        url = self.get_query_url('/dataobjects', alias=reference_obj['aliases'][0])
        queried_objs = self.dos_request('GET', url)['data_objects']
        for queried_obj in queried_objs:
            self.assertIn(reference_obj['aliases'][0], queried_obj['aliases'])

    @test_requires('ListDataObjects')
    def test_list_data_objects_with_nonexist_alias(self):
        """
        Test to ensure that looking up a nonexistent alias returns an
        empty list.
        """
        alias = str(uuid.uuid1())  # An alias that is unlikely to exist
        body = self.dos_request('GET', self.get_query_url('/dataobjects', alias=alias))
        self.assertEqual(len(body['data_objects']), 0)

    @test_requires('ListDataObjects')
    def test_list_data_objects_paging(self):
        """
        Demonstrates basic paging features.
        """
        # Test the page_size parameter
        r = self.dos_request('GET', self.get_query_url('/dataobjects', page_size=3))
        self.assertEqual(len(r['data_objects']), 3)
        r = self.dos_request('GET', self.get_query_url('/dataobjects', page_size=7))
        self.assertEqual(len(r['data_objects']), 7)

        # Next, given that the adjusting page_size works, we can test that paging
        # works by making a ListDataObjects request with page_size=2, then making
        # two requests with page_size=1, and comparing that the results are the same.
        both = self.dos_request('GET', self.get_query_url('/dataobjects', page_size=2))
        self.assertEqual(len(both['data_objects']), 2)
        first = self.dos_request('GET', self.get_query_url('/dataobjects', page_size=1))
        self.assertEqual(len(first['data_objects']), 1)
        second = self.dos_request('GET', self.get_query_url('/dataobjects', page_size=1,
                                                            page_token=first['next_page_token']))
        self.assertEqual(len(second['data_objects']), 1)
        self.assertEqual(first['data_objects'][0], both['data_objects'][0])
        self.assertEqual(second['data_objects'][0], both['data_objects'][1])

    @test_requires('ListDataObjects')
    def test_list_data_object_querying(self):
        """
        Tests if ListDataObject handles multiple query parameters correctly.
        """
        # ListDataObjects supports querying by checksum, URL, and alias.
        # To test this, let us take a data object with a unique checksum,
        # URL, and alias:
        obj, _ = self.get_random_data_object()

        def query(expected_results, expected_object=None, **kwargs):
            """
            Makes a ListDataObject query with parameters specifying
            the checksum, URL, and alias of the ``obj`` data object above.

            :param int expected_results: the amount of results to expect
                                         from the ListDataObjects request
            :param dict expected_object: if expected_results is 1, then
                                         if only one object is returned
                                         from the query, assert that the
                                         returned object is this object
            :param kwargs: query parameters for the ListDataObjects request
            """
            args = {
                'url': obj['urls'][0]['url'],
                'alias': obj['aliases'][0],
                'checksum': obj['checksums'][0]['checksum'],
                'checksum_type': obj['checksums'][0]['type']
            }
            args.update(kwargs)
            url = self.get_query_url('/dataobjects', **args)
            r = self.dos_request('GET', url)
            self.assertEqual(len(r['data_objects']), expected_results)
            if expected_object and expected_results == 1:
                self.assertEqual(expected_object, r['data_objects'][0])

        rand = str(uuid.uuid1())

        # If the data object we selected has a unique checksum, alias, and URL,
        # then when we make a ListDataObjects requesting all three of those
        # parameters, we should receive exactly one data object back - the one
        # we chose above.
        query(expected_results=1, expected_object=obj)

        # That said, if we query for the above checksum and alias but also
        # query for a URL that is unlikely to exist, then we should receive
        # no results, as the search criteria should be logically ANDed together.
        # If `expected_results != 0`, then it is likely that the criteria are
        # being ORed.
        query(expected_results=0, url=rand)

        # And to finish up the test, we repeat the test directly aforementioned
        # on the other two attributes we expect to be unique.
        query(expected_results=0, alias=rand)
        query(expected_results=0, checksum=rand)

    # # GetDataObject tests
    @test_requires('ListDataObjects', 'GetDataObject')
    def test_get_data_object(self):
        """
        Lists Data Objects and then gets one by ID.
        """
        data_obj_1, url = self.get_random_data_object()
        data_obj_2 = self.dos_request('GET', url)['data_object']
        # Test that the data object randomly chosen via `/dataobjects`
        # can be retrieved via `/dataobjects/{data_object_id}`
        self.assertEqual(data_obj_1, data_obj_2)

    @test_requires('ListDataBundles', 'GetDataBundle')
    def test_get_data_bundle(self):
        """
        Lists data bundles and then gets one by ID.
        """
        data_bdl_1, url = self.get_random_data_bundle()
        data_bdl_2 = self.dos_request('GET', url)['data_bundle']
        # Test that the data object randomly chosen via `/databundles`
        # can be retrieved via `/databundles/{data_bundle_id}`
        self.assertEqual(data_bdl_1, data_bdl_2)

    @test_requires('ListDataBundles')
    def test_list_data_bundles_with_nonexist_alias(self):
        """
        Test to ensure that searching for data bundles with a nonexistent
        alias returns an empty list.
        """
        alias = str(uuid.uuid1())  # An alias that is unlikely to exist
        body = self.dos_request('GET', self.get_query_url('/databundles', alias=alias))
        self.assertEqual(len(body['data_bundles']), 0)

    @test_requires('GetDataBundle')
    def test_get_nonexistent_data_bundle(self):
        """
        Verifies that requesting a data bundle that doesn't exist results in HTTP 404
        """
        bdl, url = self.get_random_data_bundle()
        self.dos_request('GET', '/databundles/NonexistentDataBundle',
                         body={'data_bundle': bdl}, expected_status=404)

    @test_requires('UpdateDataObject')
    def test_update_nonexistent_data_object(self):
        """
        Verifies that trying to update a data object that doesn't exist
        returns HTTP 404
        """
        obj, url = self.get_random_data_object()
        self.dos_request('PUT', '/dataobjects/NonexistentObjID', expected_status=404,
                         body={'data_object': obj, 'data_object_id': obj['id']})

    @test_requires('GetDataObject', 'ListDataObjects')
    def test_update_data_object_with_bad_request(self):
        """
        Verifies that attempting to update a data object with a malformed
        request returns HTTP 400
        """
        _, url = self.get_random_data_object()
        self.dos_request('PUT', url, expected_status=400, body={'abc': ''})

    @test_requires('ListDataObjects', 'UpdateDataObject', 'GetDataObject')
    def test_alias_update(self):
        """
        Demonstrates updating a data object with a given alias.
        """
        alias = 'daltest:' + str(uuid.uuid1())
        # First, select a "random" object that we can test
        data_object, url = self.get_random_data_object()

        # Try and update with no changes.
        self.dos_request('PUT', url, body={'data_object': data_object})
        # We specify the Content-Type since Chalice looks for it when
        # deserializing the request body server-side

        # Test adding an alias (acceptably unique to try
        # retrieving the object by the alias)
        data_object['aliases'].append(alias)

        # Try and update, this time with a change.
        update_response = self.dos_request('PUT', url,
                                           body={'data_object': data_object})
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
        data_object, url = self.get_random_data_object()

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
        self.dos_request('PUT', url, body={'data_object': data_object})
        time.sleep(2)  # Give the server some time to catch up

        # Test and see if the update took place
        get_response = self.dos_request('GET', url)['data_object']
        # We only compare the change attributes as DOS implementations
        # can update timestamps server-side
        self.assertEqual(get_response['name'], data_object['name'])
        self.assertEqual(get_response['urls'], data_object['urls'])
