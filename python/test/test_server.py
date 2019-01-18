# -*- coding: utf-8 -*-
import logging
import subprocess
import time

import bravado.exception
import jsonschema.exceptions

import ga4gh.drs
import ga4gh.drs.test
import ga4gh.drs.client

SERVER_URL = 'http://localhost:8080/ga4gh/drs/v1'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.captureWarnings(True)
# Make scrolling through test logs more useful
logging.getLogger('swagger_spec_validator.ref_validators').setLevel(logging.INFO)
logging.getLogger('bravado_core.model').setLevel(logging.INFO)
logging.getLogger('swagger_spec_validator.validator20').setLevel(logging.INFO)


class TestServer(ga4gh.drs.test.DataRepositoryServiceTest):
    @classmethod
    def setUpClass(cls):
        cls._server_process = subprocess.Popen(['ga4gh_drs_server'], stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, shell=False)
        time.sleep(2)
        local_client = ga4gh.drs.client.Client(SERVER_URL)
        cls._models = local_client.models
        cls._client = local_client.client

    @classmethod
    def tearDownClass(cls):
        logger.info('Tearing down server process (PID %d)', cls._server_process.pid)
        cls._server_process.kill()
        cls._server_process.wait()

    def generate_bundle(self, **kwargs):
        """
        Generates a Bundle with bravado.
        Same arguments as :meth:`generate_object`.
        """
        bdl_model = self._models.get_model('Bundle')
        bdl = next(self.generate_bundles(1))
        bdl.update(kwargs)
        return bdl_model.unmarshal(bdl)

    def generate_object(self, **kwargs):
        """
        Generates a Object with bravado.
        :param kwargs: fields to set in the generated data object
        """
        obj_model = self._models.get_model('Object')
        obj = next(self.generate_objects(1))
        obj.update(kwargs)
        return obj_model.unmarshal(obj)

    def request(self, operation_id, query={}, **params):
        """
        Make a request to the DOS server with :class:`ga4gh.drs.client.Client`.
        :param str operation_id: the name of the operation ID to call (e.g.
                                 ListBundles, DeleteObject, etc.)
        :param dict query: parameters to include in the query / path
        :param \*\*params: parameters to include in the request body
                           (that would normally be provided to the
                           Request model)
        :returns: response body of the request as a schema model (e.g.
                  ListBundlesResponse)
        """
        request_name = operation_id + 'Request'
        # These two in particular are special cases as they are the only
        # models that utilize query parameters
        if request_name in ['ListBundlesRequest', 'ListObjectsRequest']:
            params = self._models.get_model(request_name)(**params).marshal()
        elif request_name in self._models.swagger_spec.definitions:
            params = {'body': self._models.get_model(request_name)(**params)}
        params.update(query)
        return getattr(self._client, operation_id)(**params).result()

    def assertSameObject(self, obj_1, obj_2, check_version=True):
        """
        Verifies that the two provided data objects are the same by
        comparing them key-by-key.

        :param bool check_version: set to True to check if the version
                                   key is the same, False otherwise.
                                   This option is provided as some DOS
                                   implementations will touch the version
                                   key on their own, and some will not
        :raises AssertionError: if the provided objects are not the same
        :rtype: bool
        :returns: True if the objects are the same
        """
        # ctime and mtime can be touched server-side
        ignored = ['created', 'updated']
        if not check_version:
            ignored.append('version')
        for k in obj_1.__dict__['_Model__dict'].keys():
            if k in ignored:
                continue
            error = "Mismatch on '%s': %s != %s" % (k, obj_1[k], obj_2[k])
            self.assertEqual(obj_1[k], obj_2[k], error)
        return True

    def assertSameBundle(self, *args, **kwargs):
        """
        Wrapper around :meth:`assertSameObject`. Has the exact same
        arguments and functionality, as the method by which data objects
        and data bundles are compared are similar.

        This method is provided so that the test code can be semantically
        correct.
        """
        return self.assertSameObject(*args, **kwargs)

    def test_create_object(self):
        """Smoke test to verify functionality of the CreateObject endpoint."""
        # First, create a data object.
        obj = self.generate_object()
        response = self.request('CreateObject', object=obj)
        # Then, verify that the data object id returned by the server is the
        # same id that we sent to it.
        self.assertEqual(response['object_id'], obj.id,
                         "Mismatch between data object ID in request and response")
        # Now that we know that things look fine at the surface level,
        # verify that we can retrieve the data object by its ID.
        response = self.request('GetObject', object_id=obj.id)
        # Finally, ensure that the returned data object is the same as the
        # one we sent.
        self.assertSameObject(obj, response.object)

    def test_duplicate_checksums(self):
        """ validate expected behavior of multiple creates of same checksum """
        # Create a data object (:var:`obj_1`) and save its checksum
        # for later.
        obj_1 = self.generate_object()
        # There's some bug that causes a RecursionError if :var:`obj_1_checksum`
        # is passed to :meth:`self._client.ListObjects` without first being
        # casted to a string...
        obj_1_checksum = str(obj_1.checksums[0].checksum)
        obj_1_checksum_type = str(obj_1.checksums[0].type)
        self.request('CreateObject', object=obj_1)
        # Create another data object (:var:`obj_2`) but with the
        # same checksum as :var:`obj_1`.
        obj_2 = self.generate_object()
        obj_2.checksums[0].checksum = obj_1_checksum
        obj_2.checksums[0].type = obj_1_checksum_type
        self.request('CreateObject', object=obj_2)
        # There are now two data objects with the same checksum on the
        # server. We can retrieve them using a ListObjects request.
        # Even though we're only expecting two data objects to be
        # returned by this query, we specify a high page_size - that way,
        # if we receive more than two data objects in the response, we
        # know something is up.
        response = self.request('ListObjects', page_size=100,
                                checksum=obj_1_checksum,
                                checksum_type=obj_1_checksum_type)
        self.assertEqual(len(response.objects), 2)
        # Finally, confirm that the server returned both data objects
        # that we created, and that they're all intact.
        try:
            self.assertSameObject(obj_1, response.objects[0])
        except AssertionError:
            self.assertSameObject(obj_2, response.objects[0])
        try:
            self.assertSameObject(obj_2, response.objects[1])
        except AssertionError:
            self.assertSameObject(obj_1, response.objects[1])

    def test_update_object(self):
        # Create a data object using CreateObject, then retrieve it
        # using GetObject to make sure it exists.
        old_obj = self.generate_object()
        self.request('CreateObject', object=old_obj)
        response = self.request('GetObject', object_id=old_obj.id)
        server_obj = response.object
        self.assertSameObject(old_obj, server_obj)
        # Now that we have a shiny new data object, let's update all of
        # its attributes - we can do this quickly by generating a new
        # data object and updating all of the attributes of the old object
        # with that of the new one. (All the attributes except the id: we
        # need to be careful that the id of the data object we send in the
        # request body is the same as the original data object, or the data
        # object's id will be changed, rendering this exercise moot.)
        new_obj = self.generate_object(id=old_obj.id)
        self.request('UpdateObject', object=new_obj,
                     query={'object_id': old_obj.id})
        response = self.request('GetObject', object_id=old_obj.id)
        server_obj = response.object
        # The data object should now be updated. If we use the GetObject
        # endpoint to retrieve the updated data object from the server,
        # it should be the same as the one we have in memory.
        response = self.request('GetObject', object_id=old_obj.id)
        server_obj = response.object
        self.assertSameObject(server_obj, new_obj, check_version=False)

    # TODO: DOS server currently does not support updating a data object id but
    # it should.
    # def test_update_object_id(self):
    #     """
    #     Test that updating a data object's id works correctly
    #     """
    #     # Create a data object
    #     obj_1 = self.generate_object()
    #     self.request('CreateObject', object=obj_1)
    #     # Confirm that the data object we just created exists server-side
    #     response = self.request('GetObject', object_id=obj_1.id)
    #     self.assertSameObject(obj_1, response.object)
    #     # Update the id of the data object we created to something different
    #     obj_2 = response.object
    #     obj_2.id = 'new-data-object-id'
    #     self.request('UpdateObject', object=obj_2,
    #                  query={'object_id': obj_1.id})
    #     # Try to retrieve the data object by its new id and its old id
    #     # The former should succeed:
    #     response = self.request('GetObject', object_id=obj_2.id)
    #     self.assertSameObject(response.object, obj_2)
    #     # And the latter should fail:
    #     with self.assertRaises(bravado.exception.HTTPNotFound) as ctx:
    #         self.request('GetObject', object_id=obj_1.id)
    #     self.assertEqual(ctx.exception.status_code, 404)

    def test_object_long_serialization(self):
        # Specify `size` as an int gte 2^31 - 1 (int32 / Javascript's
        # maximum int size) but lte 2^63 - 1 (int64 / maximum int size
        # in schema) to test json serialization/casting (see #63)
        obj = self.generate_object(size=2**63 - 1)
        self.request('CreateObject', object=obj)
        # Now check to make sure that nothing was lost in transit
        retrieved_obj = self.request('GetObject', object_id=obj.id).object
        self.assertEqual(obj.size, retrieved_obj.size)

    def test_delete_object(self):
        # Create a data object
        obj = self.generate_object()
        self.request('CreateObject', object=obj)
        # Make sure it exists!
        response = self.request('GetObject', object_id=obj.id)
        self.assertSameObject(obj, response.object)
        # Begone foul data object
        self.request('DeleteObject', object_id=obj.id)
        # Make sure it's gone
        with self.assertRaises(bravado.exception.HTTPNotFound) as ctx:
            self.request('GetObject', object_id=obj.id)
        self.assertEqual(ctx.exception.status_code, 404)

    def test_list_object_querying(self):
        obj = self.generate_object()
        self.request('CreateObject', object=obj)
        # We should be able to retrieve the data object by a unique alias, ...
        results = self.request('ListObjects', query={'alias': obj.aliases[0]})
        self.assertEqual(len(results['objects']), 1)
        results = self.request('ListObjects',  # by a unique checksum...
                               query={'checksum': obj.checksums[0].checksum,
                                      'checksum_type': obj.checksums[0].type})
        self.assertEqual(len(results['objects']), 1)
        results = self.request('ListObjects',  # and by a unique url..
                               query={'url': obj.urls[0].url})
        self.assertEqual(len(results['objects']), 1)
        # The more advanced ListObjects testing is left to :meth:`ComplianceTest.test_list_object_querying`.

    def test_object_versions(self):
        obj = self.generate_object()
        self.request('CreateObject', object=obj)
        # Make a GetObjectVersions request to see retrieve all the
        # stored versions of this data object. As we've just created it,
        # there should onlty be one version.
        r = self.request('GetObjectVersions', object_id=obj.id)
        self.assertEqual(len(r['objects']), 1)
        obj.version = 'great-version'  # Now make a new version and upload it
        obj.name = 'greatest-change'  # technically unnecessary, but just in case
        self.request('UpdateObject', object=obj,
                     query={'object_id': obj.id})
        # Now that we've added another version, a GetObjectVersions
        # query should confirm that there are now two versions
        r = self.request('GetObjectVersions', object_id=obj.id)
        self.assertEqual(len(r['objects']), 2)

    def test_bundles(self):
        ids = []  # Create data objects to populate the data bundle with
        names = []
        aliases = []
        for i in range(10):
            obj = self.generate_object()
            ids.append(obj.id)
            names.append(obj.name)
            aliases.append(obj.aliases[0])
            self.request('CreateObject', object=obj)
        # Make sure that the data objects we just created exist
        for id_ in ids:
            self.request('GetObject', object_id=id_)

        # Mint a data bundle with the data objects we just created then
        # check to verify its existence
        bundle = self.generate_bundle(object_ids=ids)
        self.request('CreateBundle', bundle=bundle)
        server_bdl = self.request('GetBundle', bundle_id=bundle.id).bundle
        self.assertSameBundle(server_bdl, bundle)

        logger.info("..........Update that Bundle.................")
        server_bdl.aliases = ['ghi']
        update_bundle = server_bdl
        update_response = self.request('UpdateBundle', bundle=update_bundle,
                                       query={'bundle_id': bundle.id})
        logger.info("..........Get that Bundle.................")
        updated_bundle = self.request('GetBundle', bundle_id=update_response['bundle_id']).bundle
        logger.info('updated_bundle.aliases: %r', updated_bundle.aliases)
        logger.info('updated_bundle.updated: %r', updated_bundle.updated)
        logger.info('bundle.aliases: %r', bundle.aliases)
        logger.info('bundle.updated: %r', bundle.updated)
        self.assertEqual(updated_bundle.aliases[0], 'ghi')

        logger.info("..........List  Bundles...............")
        list_response = self.request('ListBundles')
        logger.info(len(list_response.bundles))

        logger.info("..........Get all Versions of a Bundle...............")
        versions_response = self.request('GetBundleVersions', bundle_id=bundle.id)
        logger.info(len(versions_response.bundles))

        logger.info("..........Get an Object in a Bundle..............")
        bundle = self.request('GetBundle', bundle_id=bundle.id).bundle
        object = self.request('GetObject', object_id=bundle.object_ids[0]).object
        logger.info(object.urls)

        logger.info("..........Get all Objects in a Bundle..............")
        bundle = self.request('GetBundle', bundle_id=bundle.id).bundle
        bundle_objects = []
        for object_id in bundle.object_ids:
            bundle_objects.append(self._client.GetObject(
                object_id=object_id).result().object)
        logger.info([x.name for x in bundle_objects])

        logger.info("..........Delete the Bundle...............")
        delete_response = self.request('DeleteBundle', bundle_id=bundle.id)
        logger.info(delete_response.bundle_id)
        with self.assertRaises(bravado.exception.HTTPNotFound):
            self.request('GetBundle', bundle_id=update_response['bundle_id'])

        logger.info("..........Page through a listing of  Bundles......")
        for i in range(100):
            num = "BDL{}".format(i)
            my_bundle = self.generate_bundle(name=num, aliases=[num], object_ids=bundle.object_ids)
            self.request('CreateBundle', bundle=my_bundle)
        list_response = self.request('ListBundles', page_size=10)
        ids = [x['id'] for x in list_response.bundles]
        logger.info(list_response.next_page_token)
        logger.info(ids)

        list_response = self.request('ListBundles', page_size=10, page_token=list_response.next_page_token)
        ids = [x['id'] for x in list_response.bundles]
        logger.info(ids)

        logger.info("..........List  Bundles by alias..............")
        alias_list_response = self.request('ListBundles', alias=list_response.bundles[0].aliases[0])
        logger.info(list_response.bundles[0].aliases[0])
        logger.info(alias_list_response.bundles[0].aliases[0])

    def test_list_bundle_querying(self):
        ids = []  # Create data objects to populate the data bundle with
        names = []
        aliases = []
        for i in range(10):
            obj = self.generate_object()
            ids.append(obj.id)
            names.append(obj.name)
            aliases.append(obj.aliases[0])
            self.request('CreateObject', object=obj)
        # Make sure that the data objects we just created exist
        for id_ in ids:
            self.request('GetObject', object_id=id_)

        # Mint a data bundle with the data objects we just created then
        # check to verify its existence
        bundle = self.generate_bundle(object_ids=ids)
        self.request('CreateBundle', bundle=bundle)
        results = self.request('ListBundles', query={'alias': bundle.aliases[0]})
        self.assertEqual(len(results['bundles']), 1)
        results = self.request('ListBundles',  # by a unique checksum...
                               query={'checksum': bundle.checksums[0].checksum,
                                      'checksum_type': bundle.checksums[0].type})
        self.assertEqual(len(results['bundles']), 1)

    def test_get_nonexistent_bundle(self):
        """Test querying GetBundle with a nonexistent data bundle."""
        with self.assertRaises(bravado.exception.HTTPNotFound) as ctx:
            self._client.GetBundle(bundle_id='nonexistent-key').result()
        self.assertEqual(ctx.exception.status_code, 404)

    def test_schema_required(self):
        """
        Tests that the server properly rejects a request
        missing a parameter that is marked as required.
        """
        CreateObjectRequest = self._models.get_model('CreateObjectRequest')
        Object = self._models.get_model('CreateObjectRequest')
        object = Object(name='random-name', size='1')  # Missing the `id` parameter
        create_request = CreateObjectRequest(object=object)

        with self.assertRaises(jsonschema.exceptions.ValidationError) as ctx:
            self._client.CreateObject(body=create_request)
        self.assertIn('required property', ctx.exception.message)

    def test_service_info(self):
        r = self._client.GetServiceInfo().result()
        self.assertEqual(ga4gh.drs.__version__, r.version)


class TestServerWithLocalClient(TestServer):
    """
    Runs all of the test cases in the :class:`TestServer` test suite but
    using :class:`ga4gh.drs.client.Client` when loaded locally. (In fact,
    this suite is exactly the same as :class:`TestServer` except with
    :meth:`setUpClass` modified to load the client locally.) Running all
    the same tests is a little overkill but they're fast enough that it
    really doesn't make a difference at all.
    """
    @classmethod
    def setUpClass(cls):
        cls._server_process = subprocess.Popen(['ga4gh_drs_server'], stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, shell=False)
        time.sleep(2)
        local_client = ga4gh.drs.client.Client(SERVER_URL, local=True)
        cls._models = local_client.models
        cls._client = local_client.client
