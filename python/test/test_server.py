# With app.py running start this test
from datetime import datetime
import logging
import subprocess
import time
import uuid

# setup connection, models and security
import bravado.exception
from bravado.requests_client import RequestsClient
import jsonschema.exceptions

import ga4gh.dos
import ga4gh.dos.test
from ga4gh.dos.client import Client

SERVER_URL = 'http://localhost:8080/ga4gh/dos/v1'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.captureWarnings(True)
# Make scrolling through test logs more useful
logging.getLogger('swagger_spec_validator.ref_validators').setLevel(logging.INFO)
logging.getLogger('bravado_core.model').setLevel(logging.INFO)
logging.getLogger('swagger_spec_validator.validator20').setLevel(logging.INFO)


class TestServer(ga4gh.dos.test.DataObjectServiceTest):
    @classmethod
    def setUpClass(cls):
        # start a test server
        logger.info('setting UP!!!!!!!!!!')
        p = subprocess.Popen(
            ['ga4gh_dos_server'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False)
        time.sleep(2)

        cls._server_process = p

        http_client = RequestsClient()
        # http_client.set_basic_auth(
        #   'localhost', 'admin', 'secret')
        # http_client.set_api_key(
        #   'localhost', 'XXX-YYY-ZZZ', param_in='header')
        local_client = Client(SERVER_URL, http_client=http_client)
        client = local_client.client
        models = local_client.models

        cls._models = models

        cls._client = client
        cls._local_client = local_client

    @classmethod
    def tearDownClass(cls):
        logger.info('tearing down')
        logger.info(cls._server_process.pid)
        cls._server_process.kill()
        cls._server_process.terminate()

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

    def test_client_driven_id(self):
        """ validate server uses client's id """
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataObjectRequest = self._models.get_model('CreateDataObjectRequest')
        DataObject = self._models.get_model('CreateDataObjectRequest')
        checksum = str(uuid.uuid1())
        do_id = str(uuid.uuid1())
        # CreateDataObject
        logger.info("..........Create an object............")
        create_data_object = DataObject(
            id=do_id,
            name="abc",
            size="12345",
            checksums=[Checksum(checksum=checksum, type="md5")],
            created=datetime.utcnow(),
            urls=[URL(url="a"), URL(url="b")])
        create_request = CreateDataObjectRequest(
            data_object=create_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        self.assertEqual(data_object_id, do_id, "expected server to use client's id")

    def test_duplicate_checksums(self):
        """ validate expected behavior of multiple creates of same checksum """
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataObjectRequest = self._models.get_model(
            'CreateDataObjectRequest')
        DataObject = self._models.get_model('CreateDataObjectRequest')
        checksum = str(uuid.uuid1())
        # CreateDataObject
        logger.info("..........Create an object............")
        create_data_object = DataObject(
            id=str(uuid.uuid1()),
            created=datetime.utcnow(),
            name="abc",
            size="12345",
            checksums=[Checksum(checksum=checksum, type="md5")],
            urls=[URL(url="a"), URL(url="b")])
        create_request = CreateDataObjectRequest(
            data_object=create_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        logger.info(data_object_id)
        logger.info("..........Create a 2nd  object............")
        create_data_object = DataObject(
            id=str(uuid.uuid1()),
            created=datetime.utcnow(),
            name="xyz",
            size="12345",
            checksums=[Checksum(checksum=checksum, type="md5")],
            urls=[URL(url="c")])
        create_request = CreateDataObjectRequest(
            data_object=create_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        logger.info(data_object_id)
        # ListDataObjects
        logger.info("..........List Data Objects...............")
        ListDataObjectsRequest = self._models.get_model(
            'ListDataObjectsRequest')
        next_page_token = None
        count = 0
        urls = []
        names = []
        while(True):
            list_request = ListDataObjectsRequest(checksum=checksum)
            list_request.page_size = 10
            if next_page_token:
                list_request.next_page_token = next_page_token
            list_response = self._client.ListDataObjects(
                alias=list_request.alias,
                checksum=list_request.checksum,
                checksum_type=list_request.checksum_type,
                page_size=list_request.page_size,
                page_token=list_request.page_token).result()
            next_page_token = list_response.next_page_token
            for data_object in list_response.data_objects:
                count = count + 1
                urls.extend([url.url for url in data_object.urls])
                names.append(data_object.name)
            if not list_response.next_page_token:
                break
        self.assertEqual(count, 2, 'did not return all objects for ' + checksum)
        for url in ['a', 'b', 'c']:
            self.assertIn(url, urls, 'expected {} in urls'.format(url))
        for name in ['abc', 'xyz']:
            self.assertIn(name, names, 'expected {} in names'.format(name))

    def test_create_update(self):
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataObjectRequest = self._models.get_model(
            'CreateDataObjectRequest')
        DataObject = self._models.get_model('CreateDataObjectRequest')
        # CreateDataObject
        logger.info("..........Create an object............")
        create_data_object = self.generate_populated_model('DataObject')
        create_request = CreateDataObjectRequest(
            data_object=create_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        logger.info(data_object_id)

        # GetDataObject
        logger.info("..........Get the Object we just created..............")
        get_object_response = self._client.GetDataObject(
            data_object_id=data_object_id).result()
        data_object = get_object_response.data_object
        logger.info(data_object.id)

        # UpdateDataObject
        logger.info("..........Update that object.................")
        UpdateDataObjectRequest = self._models.get_model(
            'UpdateDataObjectRequest')
        update_data_object = DataObject(
            id=str(uuid.uuid1()),
            created=datetime.utcnow(),
            name="abc",
            size="12345",
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="a"), URL(url="b"), URL(url="c")])
        update_request = UpdateDataObjectRequest(data_object=update_data_object)
        update_response = self._client.UpdateDataObject(
            data_object_id=data_object_id, body=update_request).result()
        updated_object = self._client.GetDataObject(
            data_object_id=update_response['data_object_id'])\
            .result().data_object
        logger.info(updated_object.version)
        self.assertNotEqual(updated_object.version, data_object.version)

        logger.info("..........Create another object w/ same checksum............")
        create_data_object = DataObject(
            id=str(uuid.uuid1()),
            created=datetime.utcnow(),
            name="fubar",
            size="12345",
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="foo"), URL(url="bar")])
        create_request = CreateDataObjectRequest(
            data_object=create_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        logger.info(data_object_id)

        # ListDataObjects
        logger.info("..........List Data Objects...............")
        ListDataObjectsRequest = self._models.get_model(
            'ListDataObjectsRequest')
        next_page_token = "0"
        count = 0
        while(True):
            logger.info(next_page_token)
            list_request = ListDataObjectsRequest(
                checksum='def',
                page_token=next_page_token,
                page_size=1)
            list_response = self._client.ListDataObjects(
                alias=list_request.alias,
                checksum=list_request.checksum,
                checksum_type=list_request.checksum_type,
                page_size=list_request.page_size,
                page_token=list_request.page_token,
                url=list_request.url).result()
            logger.info(list_response)
            next_page_token = list_response.next_page_token
            count += 1
            if not list_response.next_page_token:
                logger.info('done paging')
                break
        self.assertGreater(count, 1)

    def test_data_objects(self):
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataObjectRequest = self._models.get_model(
            'CreateDataObjectRequest')
        DataObject = self._models.get_model(
            'CreateDataObjectRequest')
        # CreateDataObject
        logger.info("..........Create an object............")
        create_data_object = DataObject(
            id=str(uuid.uuid1()),
            created=datetime.utcnow(),
            name="abc",
            # Specify `size` as an int greater than 2^31 - 1 (Javascript's
            # maximum int size) but lower than 2^63 - 1 (Python's maximum int
            # size) to test json serialization/casting (#63)
            size=2**63 - 2,
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="a"), URL(url="b")])
        create_request = CreateDataObjectRequest(
            data_object=create_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        logger.info(data_object_id)

        # GetDataObject
        logger.info("..........Get the Object we just created..............")
        get_object_response = self._client.GetDataObject(
            data_object_id=data_object_id).result()
        data_object = get_object_response.data_object
        logger.info(data_object.id)

        # UpdateDataObject
        logger.info("..........Update that object.................")
        UpdateDataObjectRequest = self._models.get_model(
            'UpdateDataObjectRequest')
        update_data_object = DataObject(
            id=data_object['id'],
            created=data_object['created'],
            name="abc",
            size='12345',
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="a"), URL(url="b"), URL(url="c")])
        update_request = UpdateDataObjectRequest(data_object=update_data_object)
        update_response = self._client.UpdateDataObject(
            data_object_id=data_object.id,
            body=update_request).result()
        updated_object = self._client.GetDataObject(
            data_object_id=update_response['data_object_id'])\
            .result().data_object
        logger.info(updated_object)
        logger.info(data_object)
        self.assertNotEqual(updated_object.version, data_object.version)

        # Get the old DataObject
        logger.info("..........Get the old Data Object.................")
        old_data_object = self._client.GetDataObject(
            data_object_id=update_response['data_object_id'],
            version=data_object.version).result().data_object
        logger.info(old_data_object.version)

        # ListDataObjects
        logger.info("..........List Data Objects...............")
        ListDataObjectsRequest = self._models.get_model(
            'ListDataObjectsRequest')
        list_request = ListDataObjectsRequest()
        list_response = self._client.ListDataObjects(
            alias=list_request.alias,
            checksum=list_request.checksum,
            checksum_type=list_request.checksum_type,
            page_size=list_request.page_size,
            page_token=list_request.page_token,
            url=list_request.url).result()
        logger.info(len(list_response.data_objects))
        self.assertGreater(len(list_response.data_objects), 0)

        # Get all versions of a DataObject
        logger.info("..........Get all Versions...............")
        versions_response = self._client.GetDataObjectVersions(
            data_object_id=old_data_object.id).result()
        logger.info(len(versions_response.data_objects))

        # DeleteDataObject
        logger.info("..........Delete the Object...............")
        delete_response = self._client.DeleteDataObject(
            data_object_id=data_object_id).result()
        logger.info(delete_response.data_object_id)
        try:
            self._client.GetDataObject(
                data_object_id=update_response['data_object_id']).result()
        except Exception as e:
            logger.info('The object no longer exists, 404 not found. {}'.format(e))

        # Create a Data Object specifying your own version
        logger.info(".......Create a Data Object with our own version..........")
        my_data_object = DataObject(
            id=str(uuid.uuid1()),
            created=datetime.utcnow(),
            name="abc",
            size='12345',
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="a"), URL(url="b")],
            version="great-version")
        create_request = CreateDataObjectRequest(
            data_object=my_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        data_object = self._client.GetDataObject(
            data_object_id=data_object_id).result().data_object
        logger.info(data_object.version)

        # Create a Data Object specifying your own ID
        logger.info("..........Create a Data Object with our own ID...........")
        my_data_object = DataObject(
            id="myid",
            created=datetime.utcnow(),
            file_name="abc",
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="a"), URL(url="b")],
            size=0)
        create_request = CreateDataObjectRequest(
            data_object=my_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        logger.info(data_object_id)

        # Page through a listing of data objects
        logger.info("..........Page through a listing of Objects..............")
        for i in range(100):
            my_data_object = DataObject(
                id=str(uuid.uuid1()),
                created=datetime.utcnow(),
                name="OBJ{}".format(i),
                aliases=["OBJ{}".format(i)],
                size=str(10 * i),
                checksums=[Checksum(
                    checksum="def{}".format(i), type="md5")],
                urls=[URL(url="http://{}".format(i))])
            create_request = CreateDataObjectRequest(
                data_object=my_data_object)
            self._client.CreateDataObject(
                body=create_request).result()
        list_request = ListDataObjectsRequest(page_size=10)
        list_response = self._client.ListDataObjects(
            alias=list_request.alias,
            checksum=list_request.checksum,
            checksum_type=list_request.checksum_type,
            page_size=list_request.page_size,
            page_token=list_request.page_token,
            url=list_request.url).result()
        ids = [x.id for x in list_response.data_objects]
        logger.info(list_response.next_page_token)
        logger.info(ids)

        list_request = ListDataObjectsRequest(
            page_size=10, page_token=list_response.next_page_token)
        list_response = self._client.ListDataObjects(
            alias=list_request.alias,
            checksum=list_request.checksum,
            checksum_type=list_request.checksum_type,
            page_size=list_request.page_size,
            page_token=list_request.page_token,
            url=list_request.url).result()
        ids = [x.id for x in list_response.data_objects]
        logger.info(ids)

        # Find a DataObject by alias
        logger.info("..........List Objects by alias..............")
        object_list_request = ListDataObjectsRequest(alias="OBJ1")
        object_list_response = self._client.ListDataObjects(
            alias=object_list_request.alias,
            checksum=object_list_request.checksum,
            checksum_type=object_list_request.checksum_type,
            page_size=object_list_request.page_size,
            page_token=object_list_request.page_token,
            url=object_list_request.url).result()
        logger.info(object_list_response.data_objects[0].aliases)

        # Find a DataObject by checksum
        logger.info("..........List Objects by checksum..............")
        object_list_request = ListDataObjectsRequest(
            checksum="def1")
        object_list_response = self._client.ListDataObjects(
            alias=object_list_request.alias,
            checksum=object_list_request.checksum,
            checksum_type=object_list_request.checksum_type,
            page_size=object_list_request.page_size,
            page_token=object_list_request.page_token,
            url=object_list_request.url).result()
        logger.info(object_list_response.data_objects[0].checksums)

        # Find a DataObject by URL
        logger.info("..........List Objects by url..............")
        object_list_request = ListDataObjectsRequest(url="http://1")
        object_list_response = self._client.ListDataObjects(
            alias=object_list_request.alias,
            checksum=object_list_request.checksum,
            checksum_type=object_list_request.checksum_type,
            page_size=object_list_request.page_size,
            page_token=object_list_request.page_token,
            url=object_list_request.url).result()
        logger.info(object_list_response.data_objects[0].urls)

    def test_data_bundles(self):
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataObjectRequest = self._models.get_model(
            'CreateDataObjectRequest')
        DataObject = self._models.get_model(
            'CreateDataObjectRequest')
        ListDataObjectsRequest = self._models.get_model(
            'ListDataObjectsRequest')

        logger.info("..........Create some data objects ............")
        for i in range(10):
            my_data_object = DataObject(
                id=str(uuid.uuid1()),
                created=datetime.utcnow(),
                name="OBJ{}".format(i),
                aliases=["OBJ{}".format(i)],
                size=str(10 * i),
                checksums=[Checksum(
                    checksum="def{}".format(i), type="md5")],
                urls=[URL(url="http://{}".format(i))])
            create_request = CreateDataObjectRequest(
                data_object=my_data_object)
            self._client.CreateDataObject(body=create_request).result()
        list_request = ListDataObjectsRequest(page_size=10)
        list_response = self._client.ListDataObjects(
            alias=list_request.alias,
            checksum=list_request.checksum,
            checksum_type=list_request.checksum_type,
            page_size=list_request.page_size,
            page_token=list_request.page_token,
            url=list_request.url).result()
        ids = [x.id for x in list_response.data_objects]
        logger.info(list_response.next_page_token)

        # CreateDataBundle
        logger.info("..........Create a Data Bundle............")
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataBundleRequest = self._models.get_model(
            'CreateDataBundleRequest')
        DataBundle = self._models.get_model('DataBundle')
        create_data_bundle = DataBundle(
            id=str(uuid.uuid1()),
            name="abc",
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            version=str(datetime.utcnow()),
            size="12345",
            checksums=[Checksum(checksum="def", type="md5")],
            data_object_ids=[x.id for x in list_response.data_objects])
        create_request = CreateDataBundleRequest(
            data_bundle=create_data_bundle)
        create_response = self._client.CreateDataBundle(
            body=create_request).result()
        data_bundle_id = create_response['data_bundle_id']
        logger.info(data_bundle_id)

        # GetDataBundle
        logger.info("..........Get the Bundle we just created..............")
        get_bundle_response = self._client.GetDataBundle(
            data_bundle_id=data_bundle_id).result()
        data_bundle = get_bundle_response.data_bundle
        logger.info(data_bundle)
        logger.info(data_bundle.id)

        # UpdateDataBundle
        logger.info("..........Update that Bundle.................")
        UpdateDataBundleRequest = self._models.get_model(
            'UpdateDataBundleRequest')
        update_data_bundle = DataBundle(
            id=str(uuid.uuid1()),
            name="abc",
            size="12345",
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            version=str(datetime.utcnow()),
            data_object_ids=[x.id for x in list_response.data_objects],
            checksums=[Checksum(checksum="def", type="md5")],
            aliases=["ghi"])
        update_request = UpdateDataBundleRequest(data_bundle=update_data_bundle)
        update_response = self._client.UpdateDataBundle(
            data_bundle_id=data_bundle_id,
            body=update_request).result()
        logger.info("..........Update that Bundle.................")
        updated_bundle = self._client.GetDataBundle(
            data_bundle_id=update_response['data_bundle_id'])\
            .result().data_bundle
        logger.info('updated_bundle.aliases: %r', updated_bundle.aliases)
        logger.info('updated_bundle.updated: %r', updated_bundle.updated)
        logger.info('data_bundle.aliases: %r', data_bundle.aliases)
        logger.info('data_bundle.updated: %r', data_bundle.updated)
        # logger.info(updated_bundle.version)
        # logger.info(updated_bundle.aliases)
        self.assertEqual(updated_bundle.aliases[0], 'ghi')

        # ListDataBundles
        logger.info("..........List Data Bundles...............")
        ListDataBundlesRequest = self._models.get_model(
            'ListDataBundlesRequest')
        list_request = ListDataBundlesRequest()
        list_response = self._client.ListDataBundles(
            alias=list_request.alias,
            checksum=list_request.checksum,
            checksum_type=list_request.checksum_type,
            page_size=list_request.page_size,
            page_token=list_request.page_token).result()
        logger.info(len(list_response.data_bundles))

        # Get all versions of a DataBundle
        logger.info("..........Get all Versions of a Bundle...............")
        versions_response = self._client.GetDataBundleVersions(
            data_bundle_id=data_bundle.id).result()
        logger.info(len(versions_response.data_bundles))

        # Get a DataObject from a bundle
        logger.info("..........Get an Object in a Bundle..............")
        get_bundle_response = self._client.GetDataBundle(
            data_bundle_id=data_bundle_id).result()
        data_bundle = get_bundle_response.data_bundle
        data_object = self._client.GetDataObject(
            data_object_id=data_bundle.data_object_ids[0])\
            .result().data_object
        logger.info(data_object.urls)

        # Get all DataObjects from a bundle
        logger.info("..........Get all Objects in a Bundle..............")
        get_bundle_response = self._client.GetDataBundle(
            data_bundle_id=data_bundle_id).result()
        data_bundle = get_bundle_response.data_bundle
        bundle_objects = []
        for data_object_id in data_bundle.data_object_ids:
            bundle_objects.append(self._client.GetDataObject(
                data_object_id=data_object_id).result().data_object)
        logger.info([x.name for x in bundle_objects])

        # DeleteDataBundle
        logger.info("..........Delete the Bundle...............")
        delete_response = self._client.DeleteDataBundle(
            data_bundle_id=data_bundle_id).result()
        logger.info(delete_response.data_bundle_id)
        try:
            self._client.GetDataBundle(
                data_bundle_id=update_response['data_bundle_id'])\
                .result()
        except Exception as e:
            logger.info('The object no longer exists, '
                  '404 not found. {}'.format(e))

        # Page through a listing of Data Bundles
        logger.info("..........Page through a listing of Data Bundles......")
        for i in range(100):
            my_data_bundle = DataBundle(
                id=str(uuid.uuid1()),
                created=datetime.utcnow(),
                updated=datetime.utcnow(),
                version=str(datetime.utcnow()),
                name="BDL{}".format(i),
                aliases=["BDL{}".format(i)],
                size=str(10 * i),
                data_object_ids=data_bundle.data_object_ids,
                checksums=[Checksum(
                    checksum="def", type="md5")],)
            create_request = CreateDataBundleRequest(
                data_bundle=my_data_bundle)
            self._client.CreateDataBundle(body=create_request).result()
        list_request = ListDataBundlesRequest(page_size=10)
        list_response = self._client.ListDataBundles(
            alias=list_request.alias,
            checksum=list_request.checksum,
            checksum_type=list_request.checksum_type,
            page_size=list_request.page_size,
            page_token=list_request.page_token).result()
        ids = [x['id'] for x in list_response.data_bundles]
        logger.info(list_response.next_page_token)
        logger.info(ids)

        list_request = ListDataBundlesRequest(
            page_size=10, page_token=list_response.next_page_token)
        list_response = self._client.ListDataBundles(
            alias=list_request.alias,
            checksum=list_request.checksum,
            checksum_type=list_request.checksum_type,
            page_size=list_request.page_size,
            page_token=list_request.page_token).result()
        ids = [x['id'] for x in list_response.data_bundles]
        logger.info(ids)

        # Find a DataBundle by alias
        logger.info("..........List Data Bundles by alias..............")
        list_request = ListDataBundlesRequest(
            alias=list_response.data_bundles[0].aliases[0])
        alias_list_response = self._client.ListDataBundles(
            alias=list_request.alias,
            checksum=list_request.checksum,
            checksum_type=list_request.checksum_type,
            page_size=list_request.page_size,
            page_token=list_request.page_token).result()
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
        data_object = DataObject(name=str(uuid.uuid1()), size="1")
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
        p = subprocess.Popen(['ga4gh_dos_server'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=False)
        time.sleep(2)
        cls._server_process = p

        local_client = Client(SERVER_URL, local=True)

        cls._models = local_client.models
        cls._client = local_client.client
        cls._local_client = local_client
