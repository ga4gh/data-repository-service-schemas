# -*- coding: utf-8 -*-
import json
import logging
import random
import time
try:
    import urllib.parse as urllib  # For Python 3 compat
except ImportError:
    import urllib
import uuid

import ga4gh.drs.schema
from ga4gh.drs.test import DataRepositoryServiceTest, test_requires

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AbstractComplianceTest(DataRepositoryServiceTest):
    """
    This class implements a number of compliance tests for  Object Service
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

        from ga4gh.drs.test.compliance import AbstractComplianceTest
        from chalice import LocalGateway, Config
        from my_chalice_app import chalice_app

        class TestApp(AbstractComplianceTest):
            @classmethod
            def setUpClass(cls):
                cls.lg = LocalGateway(chalice_app, Config())

            @classmethod
            def _make_request(self, meth, path, headers=None, body=None)
                headers = headers or {}
                r = self.lg.handle_request(method=meth, path='/ga4gh/drs/v1' + path,
                                           headers=headers, body=body)
                return r['body'], r['statusCode']

    You would then be able to run the compliance test suite however you
    normally run your tests (e.g. ``nosetests`` or ``python -m unittest discover``).

    :var supports: a list of supported DOS operations. By default, this is
                   the list of all DOS operations, named by the `operationId`
                   key in the schema::

                      supports = ['GetServiceInfo', 'GetBundleVersions',
                                  'CreateBundle', 'ListBundles',
                                  'UpdateObject', 'GetObject', ...]

                   Adding / removing operations from this list will adjust
                   which tests are run. So, doing something like::

                      class Test(AbstractComplianceTest):
                          self.supports = ['ListObjects']

                   would skip all tests calling UpdateBundle, GetBundle,
                   and any other endpoint that is not ListObjects.
    """
    # Populate :var:`supports` with the `operationId` of each DOS endpoint
    # specified in the schema.
    supports = []
    for path in ga4gh.drs.schema.present_schema()['paths'].values():
        for method in path.values():
            supports.append(method['operationId'])

    @classmethod
    def _make_request(cls, meth, path, headers=None, body=None):
        """
        Method that makes requests to a DOS implementation under test
        given a method, path, request headers, and a request body.

        The provided path is the path provided in the  Object Service
        schema - this means that in your implementation of this method,
        you might need to prepend the provided path with your ``basePath``,
        e.g. ``/ga4gh/drs/v1``.

        This method should return a tuple of the raw request content as a
        string and the return code of the request as an int.

        :param str meth: the HTTP method to use in the request (i.e. GET,
                         PUT, etc.)
        :param str path: path to make a request to, sans hostname (e.g.
                         `/bundles`)
        :param dict headers: headers to include with the request
        :param dict body: data to be included in the request body (serialized
                          as JSON)
        :rtype: tuple
        :returns: a tuple of the response body as a JSON-formatted string and the
                  response code as an int
        """
        raise NotImplementedError

    @classmethod
    def drs_request(cls, meth, path, headers=None, body=None, expected_status=200):
        """
        Wrapper function around :meth:`AbstractComplianceTest._make_request`.
        Logs the request being made, makes the request with
        :meth:`._make_request`, checks for errors, and performs transparent
        JSON de/serialization.

        It is assumed that any request made through this function is a
        request made to the underlying DOS implementation - e.g.,
        ``self.drs_request('https://example.com/')`` should be expected
        to fail.

        :param str meth: the HTTP method to use in the request (i.e. GET,
                         PUT, etc.)
        :param str path: path to make a request to, sans hostname (e.g.
                         `/bundles`)
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
        # :meth:`drs_request` must be an instance method. Since the only
        # advantage we really lose is a prettier error message, we can
        # be a little verbose this one time.
        # It's preferable that :meth:`drs_request` be defined as a class method
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

            >>> self.get_query_url('/objects', alias=123)
            '/objects?alias=123'

        :param str path: URL path without query parameters
        :param kwargs: query parameters
        :rtype: str
        """
        return path + '?' + urllib.urlencode(kwargs)

    def get_random_object(self):
        """
        Retrieves a 'random' data object by performing a ListObjects
        request with a large page size then randomly selecting a data
        object from the response.

        As this test utilizes the ListObjects operation, be sure to
        specify that as a test requirement with :func:`test_requires`
        when using this context manager in a test case.

        Usage::

            obj, url = self.get_random_object()

        :returns: a random data object as a dict and its relative URL
                  (e.g. '/objects/abcdefg-12345') as a string
        :rtype: tuple
        """
        r = self.drs_request('GET', self.get_query_url('/objects', page_size=100))
        obj = random.choice(r['objects'])
        url = '/objects/' + obj['id']
        return obj, url

    def get_random_bundle(self):
        """
        Retrieves a 'random' data bundle. Similar to :meth:`get_random_object`
        but retrieves a data bundle instead.
        """
        r = self.drs_request('GET', self.get_query_url('/bundles', page_size=100))
        bdl = random.choice(r['bundles'])
        url = '/bundles/' + bdl['id']
        return bdl, url

    # # ListObject tests
    @test_requires('ListObjects')
    def test_list_objects_simple(self):
        """
        Smoke test to verify that `GET /objects` returns a response.
        """
        r = self.drs_request('GET', '/objects')
        self.assertTrue(r)

    @test_requires('ListObjects')
    def test_list_objects_by_checksum(self):
        """
        Test that filtering by checksum in ListObjects works nicely.
        Since we can assume that checksums are unique between data
        objects, we can test this functionality by selecting a random
        data object then using ListObjects with a checksum parameter
        and asserting that only one result is returned and that the
        result returned is the same as the one queried.
        """
        obj, _ = self.get_random_object()
        for cs in obj['checksums']:
            url = self.get_query_url('/objects', checksum=cs['checksum'], checksum_type=cs['type'])
            r = self.drs_request('GET', url)
            self.assertEqual(len(r['objects']), 1)
            self.assertEqual(r['objects'][0]['id'], obj['id'])

    @test_requires('ListObjects')
    def test_list_objects_by_alias(self):
        """
        Tests that filtering by alias in ListObjects works. We do
        this by selecting a random data object with ListObjects
        then performing another ListObjects query but filtering
        by the alias, then checking that every returned object contains
        the proper aliases.
        """
        reference_obj, _ = self.get_random_object()
        url = self.get_query_url('/objects', alias=reference_obj['aliases'][0])
        queried_objs = self.drs_request('GET', url)['objects']
        for queried_obj in queried_objs:
            self.assertIn(reference_obj['aliases'][0], queried_obj['aliases'])

    @test_requires('ListObjects')
    def test_list_objects_with_nonexist_alias(self):
        """
        Test to ensure that looking up a nonexistent alias returns an
        empty list.
        """
        alias = str(uuid.uuid1())  # An alias that is unlikely to exist
        body = self.drs_request('GET', self.get_query_url('/objects', alias=alias))
        self.assertEqual(len(body['objects']), 0)

    @test_requires('ListObjects')
    def test_list_objects_paging(self):
        """
        Demonstrates basic paging features.
        """
        # Test the page_size parameter
        r = self.drs_request('GET', self.get_query_url('/objects', page_size=3))
        self.assertEqual(len(r['objects']), 3)
        r = self.drs_request('GET', self.get_query_url('/objects', page_size=7))
        self.assertEqual(len(r['objects']), 7)

        # Next, given that the adjusting page_size works, we can test that paging
        # works by making a ListObjects request with page_size=2, then making
        # two requests with page_size=1, and comparing that the results are the same.
        both = self.drs_request('GET', self.get_query_url('/objects', page_size=2))
        self.assertEqual(len(both['objects']), 2)
        first = self.drs_request('GET', self.get_query_url('/objects', page_size=1))
        self.assertEqual(len(first['objects']), 1)
        second = self.drs_request('GET', self.get_query_url('/objects', page_size=1,
                                                            page_token=first['next_page_token']))
        self.assertEqual(len(second['objects']), 1)
        self.assertEqual(first['objects'][0], both['objects'][0])
        self.assertEqual(second['objects'][0], both['objects'][1])

    @test_requires('ListObjects')
    def test_list_object_querying(self):
        """
        Tests if ListObject handles multiple query parameters correctly.
        """
        # ListObjects supports querying by checksum, URL, and alias.
        # To test this, let us take a data object with a unique checksum,
        # URL, and alias:
        obj, _ = self.get_random_object()

        def query(expected_results, expected_object=None, **kwargs):
            """
            Makes a ListObject query with parameters specifying
            the checksum, URL, and alias of the ``obj`` data object above.

            :param int expected_results: the amount of results to expect
                                         from the ListObjects request
            :param dict expected_object: if expected_results is 1, then
                                         if only one object is returned
                                         from the query, assert that the
                                         returned object is this object
            :param kwargs: query parameters for the ListObjects request
            """
            args = {
                'url': obj['urls'][0]['url'],
                'alias': obj['aliases'][0],
                'checksum': obj['checksums'][0]['checksum'],
                'checksum_type': obj['checksums'][0]['type']
            }
            args.update(kwargs)
            url = self.get_query_url('/objects', **args)
            r = self.drs_request('GET', url)
            self.assertEqual(len(r['objects']), expected_results)
            if expected_object and expected_results == 1:
                self.assertEqual(expected_object, r['objects'][0])

        rand = str(uuid.uuid1())

        # If the data object we selected has a unique checksum, alias, and URL,
        # then when we make a ListObjects requesting all three of those
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

    # # GetObject tests
    @test_requires('ListObjects', 'GetObject')
    def test_get_object(self):
        """
        Lists  Objects and then gets one by ID.
        """
        obj_1, url = self.get_random_object()
        obj_2 = self.drs_request('GET', url)['object']
        # Test that the data object randomly chosen via `/objects`
        # can be retrieved via `/objects/{object_id}`
        self.assertEqual(obj_1, obj_2)

    @test_requires('ListBundles', 'GetBundle')
    def test_get_bundle(self):
        """
        Lists data bundles and then gets one by ID.
        """
        bdl_1, url = self.get_random_bundle()
        bdl_2 = self.drs_request('GET', url)['bundle']
        # Test that the data object randomly chosen via `/bundles`
        # can be retrieved via `/bundles/{bundle_id}`
        self.assertEqual(bdl_1, bdl_2)

    @test_requires('ListBundles')
    def test_list_bundles_with_nonexist_alias(self):
        """
        Test to ensure that searching for data bundles with a nonexistent
        alias returns an empty list.
        """
        alias = str(uuid.uuid1())  # An alias that is unlikely to exist
        body = self.drs_request('GET', self.get_query_url('/bundles', alias=alias))
        self.assertEqual(len(body['bundles']), 0)

    @test_requires('GetBundle')
    def test_get_nonexistent_bundle(self):
        """
        Verifies that requesting a data bundle that doesn't exist results in HTTP 404
        """
        bdl, url = self.get_random_bundle()
        self.drs_request('GET', '/bundles/NonexistentBundle',
                         body={'bundle': bdl}, expected_status=404)

    @test_requires('UpdateObject')
    def test_update_nonexistent_object(self):
        """
        Verifies that trying to update a data object that doesn't exist
        returns HTTP 404
        """
        obj, url = self.get_random_object()
        self.drs_request('PUT', '/objects/NonexistentObjID', expected_status=404,
                         body={'object': obj, 'object_id': obj['id']})

    @test_requires('GetObject', 'ListObjects')
    def test_update_object_with_bad_request(self):
        """
        Verifies that attempting to update a data object with a malformed
        request returns HTTP 400
        """
        _, url = self.get_random_object()
        self.drs_request('PUT', url, expected_status=400, body={'abc': ''})

    @test_requires('ListObjects', 'UpdateObject', 'GetObject')
    def test_alias_update(self):
        """
        Demonstrates updating a data object with a given alias.
        """
        alias = 'daltest:' + str(uuid.uuid1())
        # First, select a "random" object that we can test
        object, url = self.get_random_object()

        # Try and update with no changes.
        self.drs_request('PUT', url, body={'object': object})
        # We specify the Content-Type since Chalice looks for it when
        # deserializing the request body server-side

        # Test adding an alias (acceptably unique to try
        # retrieving the object by the alias)
        object['aliases'].append(alias)

        # Try and update, this time with a change.
        update_response = self.drs_request('PUT', url,
                                           body={'object': object})
        self.assertEqual(object['id'], update_response['object_id'])

        time.sleep(2)

        # Test and see if the update took place by retrieving the object
        # and checking its aliases
        get_response = self.drs_request('GET', url)
        self.assertEqual(update_response['object_id'], get_response['object']['id'])
        self.assertIn(alias, get_response['object']['aliases'])

        # Testing the update again by using a DOS ListObjectsRequest
        # to locate the object by its new alias.
        list_request = {
            'alias': alias,
            # We know the alias is unique, so even though page_size > 1
            # we expect only one result.
            'page_size': 10
        }
        list_url = self.get_query_url('/objects', **list_request)
        list_response = self.drs_request('GET', list_url)
        self.assertEqual(1, len(list_response['objects']))
        self.assertIn(alias, list_response['objects'][0]['aliases'])

        # # Tear down and remove the test alias
        # params['body']['object']['aliases'].remove(alias)
        # self.drs_request('PUT', url, **params)

    @test_requires('ListObjects', 'UpdateObject')
    def test_full_object_update(self):
        """
        Demonstrates updating multiple fields of a data object at once.
        This incidentally also tests object conversion.
        """
        # First, select a "random" object that we can test
        object, url = self.get_random_object()

        # Make a new data object that is different from the data object we retrieved
        attributes = {
            # 'name' and 'description' are optional fields and might not be present
            'name': object.get('name', '') + 'test-suffix',
            # See Biosphere/drs-azul-lambda#87
            # 'description': object.get('description', '') + 'Change This',
            'urls': [
                {'url': 'https://cgl.genomics.ucsc.edu/'},
                {'url': 'https://github.com/Biosphere'}
            ]
        }
        object.update(attributes)

        # Now update the old data object with the new attributes we added
        self.drs_request('PUT', url, body={'object': object})
        time.sleep(2)  # Give the server some time to catch up

        # Test and see if the update took place
        get_response = self.drs_request('GET', url)['object']
        # We only compare the change attributes as DOS implementations
        # can update timestamps server-side
        self.assertEqual(get_response['name'], object['name'])
        self.assertEqual(get_response['urls'], object['urls'])
