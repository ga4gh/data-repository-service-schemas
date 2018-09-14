# -*- coding: utf-8 -*-
import logging
import subprocess
import time

import bravado.exception
import jsonschema.exceptions

import ga4gh.dos
import ga4gh.dos.test
import ga4gh.dos.client

SERVER_URL = 'http://localhost:8080/ga4gh/dos/v1'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.captureWarnings(True)
# Make scrolling through test logs more useful
logging.getLogger('swagger_spec_validator.ref_validators').setLevel(logging.INFO)
logging.getLogger('bravado_core.model').setLevel(logging.INFO)
logging.getLogger('swagger_spec_validator.validator20').setLevel(logging.INFO)


class TestServer(ga4gh.dos.test.DataObjectServiceTest):
    @classmethod
    def setUpClass(cls):
        # Start a test server
        cls._server_process = subprocess.Popen(['ga4gh_dos_server'], stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, shell=False)
        time.sleep(2)
        # Set up the client
        local_client = ga4gh.dos.client.Client(SERVER_URL)
        cls._models = local_client.models
        cls._client = local_client.client

    @classmethod
    def tearDownClass(cls):
        logger.info('Tearing down server process (PID %d)', cls._server_process.pid)
        cls._server_process.kill()
        cls._server_process.wait()

    def generate_data_bundle(self, **kwargs):
        """
        Generates a DataBundle with bravado.
        Same arguments as :meth:`generate_data_object`.
        """
        data_bdl_model = self._models.get_model('DataBundle')
        data_bdl = next(self.generate_data_bundles(1))
        data_bdl.update(kwargs)
        return data_bdl_model.unmarshal(data_bdl)

    def generate_data_object(self, **kwargs):
        """
        Generates a DataObject with bravado.
        :param kwargs: fields to set in the generated data object
        """
        data_obj_model = self._models.get_model('DataObject')
        data_obj = next(self.generate_data_objects(1))
        data_obj.update(kwargs)
        return data_obj_model.unmarshal(data_obj)

    def request(self, operation_id, query={}, **params):
        """
        Make a request to the DOS server with :class:`ga4gh.dos.client.Client`.
        :param str operation_id: the name of the operation ID to call (e.g.
                                 ListDataBundles, DeleteDataObject, etc.)
        :param dict query: parameters to include in the query / path
        :param \*\*params: parameters to include in the request body
                           (that would normally be provided to the
                           Request model)
        :returns: response body of the request as a schema model (e.g.
                  ListDataBundlesResponse)
        """
        request_name = operation_id + 'Request'
        # These two in particular are special cases as they are the only
        # models that utilize query parameters
        if request_name in ['ListDataBundlesRequest', 'ListDataObjectsRequest']:
            params = self._models.get_model(request_name)(**params).marshal()
        elif request_name in self._models.swagger_spec.definitions:
            params = {'body': self._models.get_model(request_name)(**params)}
        params.update(query)
        return getattr(self._client, operation_id)(**params).result()

    def assertSameDataObject(self, data_obj_1, data_obj_2, check_version=True):
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
        for k in data_obj_1.__dict__['_Model__dict'].keys():
            if k in ignored:
                continue
            error = "Mismatch on '%s': %s != %s" % (k, data_obj_1[k], data_obj_2[k])
            self.assertEqual(data_obj_1[k], data_obj_2[k], error)
        return True

    def assertSameDataBundle(self, *args, **kwargs):
        """
        Wrapper around :meth:`assertSameDataObject`. Has the exact same
        arguments and functionality, as the method by which data objects
        and data bundles are compared are similar.

        This method is provided so that the test code can be semantically
        correct.
        """
        return self.assertSameDataObject(*args, **kwargs)

    def test_create_data_object(self):
        """Smoke test to verify functionality of the CreateDataObject endpoint."""
        # First, create a data object.
        data_obj = self.generate_data_object()
        response = self.request('CreateDataObject', data_object=data_obj)
        # Then, verify that the data object id returned by the server is the
        # same id that we sent to it.
        self.assertEqual(response['data_object_id'], data_obj.id,
                         "Mismatch between data object ID in request and response")
        # Now that we know that things look fine at the surface level,
        # verify that we can retrieve the data object by its ID.
        response = self.request('GetDataObject', data_object_id=data_obj.id)
        # Finally, ensure that the returned data object is the same as the
        # one we sent.
        self.assertSameDataObject(data_obj, response.data_object)

    def test_duplicate_checksums(self):
        """ validate expected behavior of multiple creates of same checksum """
        # Create a data object (:var:`data_obj_1`) and save its checksum
        # for later.
        data_obj_1 = self.generate_data_object()
        # There's some bug that causes a RecursionError if :var:`data_obj_1_checksum`
        # is passed to :meth:`self._client.ListDataObjects` without first being
        # casted to a string...
        data_obj_1_checksum = str(data_obj_1.checksums[0].checksum)
        data_obj_1_checksum_type = str(data_obj_1.checksums[0].type)
        self.request('CreateDataObject', data_object=data_obj_1)
        # Create another data object (:var:`data_obj_2`) but with the
        # same checksum as :var:`data_obj_1`.
        data_obj_2 = self.generate_data_object()
        data_obj_2.checksums[0].checksum = data_obj_1_checksum
        data_obj_2.checksums[0].type = data_obj_1_checksum_type
        self.request('CreateDataObject', data_object=data_obj_2)
        # There are now two data objects with the same checksum on the
        # server. We can retrieve them using a ListDataObjects request.
        # Even though we're only expecting two data objects to be
        # returned by this query, we specify a high page_size - that way,
        # if we receive more than two data objects in the response, we
        # know something is up.
        response = self.request('ListDataObjects', page_size=100,
                                checksum=data_obj_1_checksum,
                                checksum_type=data_obj_1_checksum_type)
        self.assertEqual(len(response.data_objects), 2)
        # Finally, confirm that the server returned both data objects
        # that we created, and that they're all intact.
        try:
            self.assertSameDataObject(data_obj_1, response.data_objects[0])
        except AssertionError:
            self.assertSameDataObject(data_obj_2, response.data_objects[0])
        try:
            self.assertSameDataObject(data_obj_2, response.data_objects[1])
        except AssertionError:
            self.assertSameDataObject(data_obj_1, response.data_objects[1])

    def test_update_data_object(self):
        # Create a data object using CreateDataObject, then retrieve it
        # using GetDataObject to make sure it exists.
        old_data_obj = self.generate_data_object()
        self.request('CreateDataObject', data_object=old_data_obj)
        response = self.request('GetDataObject', data_object_id=old_data_obj.id)
        server_data_obj = response.data_object
        self.assertSameDataObject(old_data_obj, server_data_obj)
        # Now that we have a shiny new data object, let's update all of
        # its attributes - we can do this quickly by generating a new
        # data object and updating all of the attributes of the old object
        # with that of the new one. (All the attributes except the id: we
        # need to be careful that the id of the data object we send in the
        # request body is the same as the original data object, or the data
        # object's id will be changed, rendering this exercise moot.)
        new_data_obj = self.generate_data_object(id=old_data_obj.id)
        self.request('UpdateDataObject', data_object=new_data_obj,
                     query={'data_object_id': old_data_obj.id})
        response = self.request('GetDataObject', data_object_id=old_data_obj.id)
        server_data_obj = response.data_object
        # The data object should now be updated. If we use the GetDataObject
        # endpoint to retrieve the updated data object from the server,
        # it should be the same as the one we have in memory.
        response = self.request('GetDataObject', data_object_id=old_data_obj.id)
        server_data_obj = response.data_object
        self.assertSameDataObject(server_data_obj, new_data_obj, check_version=False)

    # DOS server currently does not support updating a data object id but
    # should
    # def test_update_data_object_id(self):
    #     """
    #     Test that updating a data object's id works correctly
    #     """
    #     # Create a data object
    #     data_obj_1 = self.generate_data_object()
    #     self.request('CreateDataObject', data_object=data_obj_1)
    #     # Confirm that the data object we just created exists server-side
    #     response = self.request('GetDataObject', data_object_id=data_obj_1.id)
    #     self.assertSameDataObject(data_obj_1, response.data_object)
    #     # Update the id of the data object we created to something different
    #     data_obj_2 = response.data_object
    #     data_obj_2.id = 'new-data-object-id'
    #     self.request('UpdateDataObject', data_object=data_obj_2,
    #                  query={'data_object_id': data_obj_1.id})
    #     # Try to retrieve the data object by its new id and its old id
    #     # The former should succeed:
    #     response = self.request('GetDataObject', data_object_id=data_obj_2.id)
    #     self.assertSameDataObject(response.data_object, data_obj_2)
    #     # And the latter should fail:
    #     with self.assertRaises(bravado.exception.HTTPNotFound) as ctx:
    #         self.request('GetDataObject', data_object_id=data_obj_1.id)
    #     self.assertEqual(ctx.exception.status_code, 404)

    def test_data_object_long_serialization(self):
        # Specify `size` as an int gte 2^31 - 1 (int32 / Javascript's
        # maximum int size) but lte 2^63 - 1 (int64 / maximum int size
        # in schema) to test json serialization/casting (see #63)
        data_obj = self.generate_data_object(size=2**63 - 1)
        self.request('CreateDataObject', data_object=data_obj)
        # Now check to make sure that nothing was lost in transit
        retrieved_obj = self.request('GetDataObject', data_object_id=data_obj.id).data_object
        self.assertEqual(data_obj.size, retrieved_obj.size)

    def test_delete_data_object(self):
        # Create a data object
        data_obj = self.generate_data_object()
        self.request('CreateDataObject', data_object=data_obj)
        # Make sure it exists!
        response = self.request('GetDataObject', data_object_id=data_obj.id)
        self.assertSameDataObject(data_obj, response.data_object)
        # Begone foul data object
        self.request('DeleteDataObject', data_object_id=data_obj.id)
        # Make sure it's gone
        with self.assertRaises(bravado.exception.HTTPNotFound) as ctx:
            self.request('GetDataObject', data_object_id=data_obj.id)
        self.assertEqual(ctx.exception.status_code, 404)

    def test_list_data_object_querying(self):
        # Create a data object
        data_obj = self.generate_data_object()
        self.request('CreateDataObject', data_object=data_obj)
        # We should be able to retrieve the data object by a unique alias, ...
        results = self.request('ListDataObjects', query={'alias': data_obj.aliases[0]})
        self.assertEqual(len(results['data_objects']), 1)
        # by a unique checksum, ...
        results = self.request('ListDataObjects',
                               query={'checksum': data_obj.checksums[0].checksum,
                                      'checksum_type': data_obj.checksums[0].type})
        self.assertEqual(len(results['data_objects']), 1)
        # and by a unique url.
        results = self.request('ListDataObjects', query={'url': data_obj.urls[0].url})
        self.assertEqual(len(results['data_objects']), 1)
        # The more advanced ListDataObjects testing is left to
        # :meth:`ga4gh.dos.test.ComplianceTest.test_list_data_object_querying`.

    def test_data_object_versions(self):
        # Create a data object
        data_obj = self.generate_data_object()
        self.request('CreateDataObject', data_object=data_obj)
        # Get all of its versions. There should only be one - the original version
        r = self.request('GetDataObjectVersions', data_object_id=data_obj.id)
        self.assertEqual(len(r['data_objects']), 1)
        # Now make a new version and upload it
        data_obj.version = 'great-version'
        data_obj.name = 'greatest-change'  # technically unnecessary, but just in case
        self.request('UpdateDataObject', data_object=data_obj,
                     query={'data_object_id': data_obj.id})
        # If we check, there should now be two versions
        r = self.request('GetDataObjectVersions', data_object_id=data_obj.id)
        self.assertEqual(len(r['data_objects']), 2)

    def test_data_bundles(self):
        # Create data objects to populate the data bundle with
        ids = []
        names = []
        aliases = []
        for i in range(10):
            data_obj = self.generate_data_object()
            ids.append(data_obj.id)
            names.append(data_obj.name)
            aliases.append(data_obj.aliases[0])
            self.request('CreateDataObject', data_object=data_obj)
        # Make sure that the data objects we just created exist
        for id_ in ids:
            self.request('GetDataObject', data_object_id=id_)

        # Mint a data bundle with the data objects we just created
        data_bundle = self.generate_data_bundle(data_object_ids=ids)
        self.request('CreateDataBundle', data_bundle=data_bundle)
        # Does the data bundle we just created exist?
        server_bdl = self.request('GetDataBundle', data_bundle_id=data_bundle.id).data_bundle
        self.assertSameDataBundle(server_bdl, data_bundle)

        # UpdateDataBundle
        logger.info("..........Update that Bundle.................")
        server_bdl.aliases = ['ghi']
        update_data_bundle = server_bdl
        update_response = self.request('UpdateDataBundle', data_bundle=update_data_bundle,
                                       query={'data_bundle_id': data_bundle.id})
        logger.info("..........Get that Bundle.................")
        updated_bundle = self.request('GetDataBundle', data_bundle_id=update_response['data_bundle_id']).data_bundle
        logger.info('updated_bundle.aliases: %r', updated_bundle.aliases)
        logger.info('updated_bundle.updated: %r', updated_bundle.updated)
        logger.info('data_bundle.aliases: %r', data_bundle.aliases)
        logger.info('data_bundle.updated: %r', data_bundle.updated)
        # logger.info(updated_bundle.version)
        # logger.info(updated_bundle.aliases)
        self.assertEqual(updated_bundle.aliases[0], 'ghi')

        # ListDataBundles
        logger.info("..........List Data Bundles...............")
        list_response = self.request('ListDataBundles')
        logger.info(len(list_response.data_bundles))

        # Get all versions of a DataBundle
        logger.info("..........Get all Versions of a Bundle...............")
        versions_response = self.request('GetDataBundleVersions', data_bundle_id=data_bundle.id)
        logger.info(len(versions_response.data_bundles))

        # Get a DataObject from a bundle
        logger.info("..........Get an Object in a Bundle..............")
        data_bundle = self.request('GetDataBundle', data_bundle_id=data_bundle.id).data_bundle
        data_object = self.request('GetDataObject', data_object_id=data_bundle.data_object_ids[0]).data_object
        logger.info(data_object.urls)

        # Get all DataObjects from a bundle
        logger.info("..........Get all Objects in a Bundle..............")
        data_bundle = self.request('GetDataBundle', data_bundle_id=data_bundle.id).data_bundle
        bundle_objects = []
        for data_object_id in data_bundle.data_object_ids:
            bundle_objects.append(self._client.GetDataObject(
                data_object_id=data_object_id).result().data_object)
        logger.info([x.name for x in bundle_objects])

        # DeleteDataBundle
        logger.info("..........Delete the Bundle...............")
        delete_response = self.request('DeleteDataBundle', data_bundle_id=data_bundle.id)
        logger.info(delete_response.data_bundle_id)
        with self.assertRaises(bravado.exception.HTTPNotFound):
            self.request('GetDataBundle', data_bundle_id=update_response['data_bundle_id'])

        # Page through a listing of Data Bundles
        logger.info("..........Page through a listing of Data Bundles......")
        for i in range(100):
            num = "BDL{}".format(i)
            my_data_bundle = self.generate_data_bundle(name=num, aliases=[num], data_object_ids=data_bundle.data_object_ids)
            self.request('CreateDataBundle', data_bundle=my_data_bundle)
        list_response = self.request('ListDataBundles', page_size=10)
        ids = [x['id'] for x in list_response.data_bundles]
        logger.info(list_response.next_page_token)
        logger.info(ids)

        list_response = self.request('ListDataBundles', page_size=10, page_token=list_response.next_page_token)
        ids = [x['id'] for x in list_response.data_bundles]
        logger.info(ids)

        # Find a DataBundle by alias
        logger.info("..........List Data Bundles by alias..............")
        alias_list_response = self.request('ListDataBundles', alias=list_response.data_bundles[0].aliases[0])
        logger.info(list_response.data_bundles[0].aliases[0])
        logger.info(alias_list_response.data_bundles[0].aliases[0])

    def test_get_nonexistent_databundle(self):
        """Test querying GetDataBundle with a nonexistent data bundle."""
        with self.assertRaises(bravado.exception.HTTPNotFound) as ctx:
            self._client.GetDataBundle(data_bundle_id='nonexistent-key').result()
        self.assertEqual(ctx.exception.status_code, 404)

    def test_schema_required(self):
        """
        Tests that the server properly rejects a request
        missing a parameter that is marked as required.
        """
        CreateDataObjectRequest = self._models.get_model('CreateDataObjectRequest')
        DataObject = self._models.get_model('CreateDataObjectRequest')
        # Missing the `id` parameter
        data_object = DataObject(name='random-name', size='1')
        create_request = CreateDataObjectRequest(data_object=data_object)

        with self.assertRaises(jsonschema.exceptions.ValidationError) as ctx:
            self._client.CreateDataObject(body=create_request)
        self.assertIn('required property', ctx.exception.message)

    def test_service_info(self):
        r = self._client.GetServiceInfo().result()
        self.assertEqual(ga4gh.dos.__version__, r.version)


class TestServerWithLocalClient(TestServer):
    """
    Runs all of the test cases in the :class:`TestServer` test suite but
    using :class:`ga4gh.dos.client.Client` when loaded locally. (In fact,
    this suite is exactly the same as :class:`TestServer` except with
    :meth:`setUpClass` modified to load the client locally.) Running all
    the same tests is a little overkill but they're fast enough that it
    really doesn't make a difference at all.
    """
    @classmethod
    def setUpClass(cls):
        # Start a test server
        cls._server_process = subprocess.Popen(['ga4gh_dos_server'], stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, shell=False)
        time.sleep(2)
        # Set up the client
        local_client = ga4gh.dos.client.Client(SERVER_URL, local=True)
        cls._models = local_client.models
        cls._client = local_client.client
