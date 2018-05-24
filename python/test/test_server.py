# With app.py running start this test
import logging
import uuid
import unittest
import subprocess
import time

# setup connection, models and security
from bravado.requests_client import RequestsClient
from bravado.exception import HTTPNotFound

from ga4gh.dos.client import Client

SERVER_URL = 'http://localhost:8080/ga4gh/dos/v1'


class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # start a test server
        print('setting UP!!!!!!!!!!')
        p = subprocess.Popen(
            ['ga4gh_dos_server'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False)
        time.sleep(2)
        # print(p.poll(), p.pid)
        cls._server_process = p

        http_client = RequestsClient()
        # http_client.set_basic_auth(
        #   'localhost', 'admin', 'secret')
        # http_client.set_api_key(
        #   'localhost', 'XXX-YYY-ZZZ', param_in='header')
        local_client = Client(SERVER_URL, http_client=http_client)
        client = local_client.client
        models = local_client.models

        # setup logging
        root = logging.getLogger()
        root.setLevel(logging.ERROR)
        logging.captureWarnings(True)
        cls._models = models

        cls._client = client
        cls._local_client = local_client

    @classmethod
    def tearDownClass(cls):
        print('tearing down')
        print(cls._server_process.pid)
        cls._server_process.kill()
        cls._server_process.terminate()

    def test_client_driven_id(self):
        """ validate server uses client's id """
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataObjectRequest = self._models.get_model(
            'CreateDataObjectRequest')
        DataObject = self._models.get_model('CreateDataObjectRequest')
        checksum = str(uuid.uuid1())
        id = str(uuid.uuid1())
        # CreateDataObject
        print("..........Create an object............")
        create_data_object = DataObject(
            id=id,
            name="abc",
            size="12345",
            checksums=[Checksum(checksum=checksum, type="md5")],
            urls=[URL(url="a"), URL(url="b")])
        create_request = CreateDataObjectRequest(
            data_object=create_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        assert data_object_id == id,  "expected server to use client's id"

    def test_duplicate_checksums(self):
        """ validate expected behavior of multiple creates of same checksum """
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataObjectRequest = self._models.get_model(
            'CreateDataObjectRequest')
        DataObject = self._models.get_model('CreateDataObjectRequest')
        checksum = str(uuid.uuid1())
        # CreateDataObject
        print("..........Create an object............")
        create_data_object = DataObject(
            name="abc",
            size="12345",
            checksums=[Checksum(checksum=checksum, type="md5")],
            urls=[URL(url="a"), URL(url="b")])
        create_request = CreateDataObjectRequest(
            data_object=create_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        print(data_object_id)
        print("..........Create a 2nd  object............")
        create_data_object = DataObject(
            name="xyz",
            size="12345",
            checksums=[Checksum(checksum=checksum, type="md5")],
            urls=[URL(url="c")])
        create_request = CreateDataObjectRequest(
            data_object=create_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        print(data_object_id)
        # ListDataObjects
        print("..........List Data Objects...............")
        ListDataObjectsRequest = self._models.get_model(
            'ListDataObjectsRequest')
        next_page_token = None
        count = 0
        urls = []
        names = []
        while(True):
            list_request = ListDataObjectsRequest(
                checksum={'checksum': checksum})
            list_request.page_size = 10
            if next_page_token:
                list_request.next_page_token = next_page_token
            list_response = self._client.ListDataObjects(
                body=list_request).result()
            next_page_token = list_response.next_page_token
            for data_object in list_response.data_objects:
                count = count + 1
                urls.extend([url.url for url in data_object.urls])
                names.append(data_object.name)
            if not list_response.next_page_token:
                break
        assert count == 2, 'did not return all objects for {}'.format(checksum)
        for url in ['a', 'b', 'c']:
            assert url in urls, 'expected {} in urls'.format(url)
        for name in ['abc', 'xyz']:
            assert name in names, 'expected {} in names'.format(name)

    def test_create_update(self):
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataObjectRequest = self._models.get_model(
            'CreateDataObjectRequest')
        DataObject = self._models.get_model('CreateDataObjectRequest')
        # CreateDataObject
        print("..........Create an object............")
        create_data_object = DataObject(
            name="abc",
            size="12345",
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="a"), URL(url="b")],
            version="0")
        create_request = CreateDataObjectRequest(
            data_object=create_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        print(data_object_id)

        # GetDataObject
        print("..........Get the Object we just created..............")
        get_object_response = self._client.GetDataObject(
            data_object_id=data_object_id).result()
        data_object = get_object_response.data_object
        print(data_object.id)

        # UpdateDataObject
        print("..........Update that object.................")
        UpdateDataObjectRequest = self._models.get_model(
            'UpdateDataObjectRequest')
        update_data_object = DataObject(
            name="abc",
            size="12345",
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="a"), URL(url="b"), URL(url="c")])
        update_request = UpdateDataObjectRequest(
            data_object=update_data_object)
        update_response = self._client.UpdateDataObject(
            data_object_id=data_object_id, body=update_request).result()
        updated_object = self._client.GetDataObject(
            data_object_id=update_response['data_object_id'])\
            .result().data_object
        print(updated_object.version)
        assert not updated_object.version == data_object.version

        print("..........Create another object w/ same checksum............")
        create_data_object = DataObject(
            name="fubar",
            size="12345",
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="foo"), URL(url="bar")])
        create_request = CreateDataObjectRequest(
            data_object=create_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        print(data_object_id)

        # ListDataObjects
        print("..........List Data Objects...............")
        ListDataObjectsRequest = self._models.get_model(
            'ListDataObjectsRequest')
        next_page_token = "0"
        count = 0
        while(True):
            print(next_page_token)
            list_request = ListDataObjectsRequest(
                checksum={'checksum': "def"},
                page_token=next_page_token,
                page_size=1)
            list_response = self._client.ListDataObjects(
                body=list_request).result()
            print(list_response)
            next_page_token = list_response.next_page_token
            count += 1
            if not list_response.next_page_token:
                print('done paging')
                break
        assert count > 1

    def test_data_objects(self):
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataObjectRequest = self._models.get_model(
            'CreateDataObjectRequest')
        DataObject = self._models.get_model(
            'CreateDataObjectRequest')
        # CreateDataObject
        print("..........Create an object............")
        create_data_object = DataObject(
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
        print(data_object_id)

        # GetDataObject
        print("..........Get the Object we just created..............")
        get_object_response = self._client.GetDataObject(
            data_object_id=data_object_id).result()
        data_object = get_object_response.data_object
        print(data_object.id)

        # UpdateDataObject
        print("..........Update that object.................")
        UpdateDataObjectRequest = self._models.get_model(
            'UpdateDataObjectRequest')
        update_data_object = DataObject(
            name="abc",
            size='12345',
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="a"), URL(url="b"), URL(url="c")])
        update_request = UpdateDataObjectRequest(
            data_object=update_data_object)
        update_response = self._client.UpdateDataObject(
            data_object_id=data_object.id,
            body=update_request).result()
        updated_object = self._client.GetDataObject(
            data_object_id=update_response['data_object_id'])\
            .result().data_object
        print(updated_object)
        print(data_object)
        assert not updated_object.version == data_object.version

        # Get the old DataObject
        print("..........Get the old Data Object.................")
        old_data_object = self._client.GetDataObject(
            data_object_id=update_response['data_object_id'],
            version=data_object.version).result().data_object
        print(old_data_object.version)

        # ListDataObjects
        print("..........List Data Objects...............")
        ListDataObjectsRequest = self._models.get_model(
            'ListDataObjectsRequest')
        list_request = ListDataObjectsRequest()
        list_response = self._client.ListDataObjects(
            body=list_request).result()
        print(len(list_response.data_objects))
        assert len(list_response.data_objects) > 0

        # Get all versions of a DataObject
        print("..........Get all Versions...............")
        versions_response = self._client.GetDataObjectVersions(
            data_object_id=old_data_object.id).result()
        print(len(versions_response.data_objects))

        # DeleteDataObject
        print("..........Delete the Object...............")
        delete_response = self._client.DeleteDataObject(
            data_object_id=data_object_id).result()
        print(delete_response.data_object_id)
        try:
            self._client.GetDataObject(
                data_object_id=update_response['data_object_id']).result()
        except Exception as e:
            print('The object no longer exists, 404 not found. {}'.format(e))

        # Create a Data Object specifying your own version
        print(".......Create a Data Object with our own version..........")
        my_data_object = DataObject(
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
        print(data_object.version)

        # Create a Data Object specifying your own ID
        print("..........Create a Data Object with our own ID...........")
        my_data_object = DataObject(
            id="myid",
            file_name="abc",
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="a"), URL(url="b")])
        create_request = CreateDataObjectRequest(
            data_object=my_data_object)
        create_response = self._client.CreateDataObject(
            body=create_request).result()
        data_object_id = create_response['data_object_id']
        print(data_object_id)

        # Page through a listing of data objects
        print("..........Page through a listing of Objects..............")
        for i in range(100):
            my_data_object = DataObject(
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
            body=list_request).result()
        ids = [x.id for x in list_response.data_objects]
        print(list_response.next_page_token)
        print(ids)

        list_request = ListDataObjectsRequest(
            page_size=10, page_token=list_response.next_page_token)
        list_response = self._client.ListDataObjects(
            body=list_request).result()
        ids = [x.id for x in list_response.data_objects]
        print(ids)

        # Find a DataObject by alias
        print("..........List Objects by alias..............")
        object_list_request = ListDataObjectsRequest(alias="OBJ1")
        object_list_response = self._client.ListDataObjects(
            body=object_list_request).result()
        print(object_list_response.data_objects[0].aliases)

        # Find a DataObject by checksum
        print("..........List Objects by checksum..............")
        object_list_request = ListDataObjectsRequest(
            checksum=Checksum(checksum="def1"))
        object_list_response = self._client.ListDataObjects(
            body=object_list_request).result()
        print(object_list_response.data_objects[0].checksums)

        # Find a DataObject by URL
        print("..........List Objects by url..............")
        object_list_request = ListDataObjectsRequest(url="http://1")
        object_list_response = self._client.ListDataObjects(
            body=object_list_request).result()
        print(object_list_response.data_objects[0].urls)

    def test_data_bundles(self):
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataObjectRequest = self._models.get_model(
            'CreateDataObjectRequest')
        DataObject = self._models.get_model(
            'CreateDataObjectRequest')
        ListDataObjectsRequest = self._models.get_model(
            'ListDataObjectsRequest')

        print("..........Create some data objects ............")
        for i in range(10):
            my_data_object = DataObject(
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
            body=list_request).result()
        ids = [x.id for x in list_response.data_objects]
        print(list_response.next_page_token)

        # CreateDataBundle
        print("..........Create a Data Bundle............")
        Checksum = self._models.get_model('Checksum')
        URL = self._models.get_model('URL')
        CreateDataBundleRequest = self._models.get_model(
            'CreateDataBundleRequest')
        DataBundle = self._models.get_model('DataBundle')
        create_data_bundle = DataBundle(
            name="abc",
            size="12345",
            checksums=[Checksum(checksum="def", type="md5")],
            data_object_ids=[x.id for x in list_response.data_objects])
        create_request = CreateDataBundleRequest(
            data_bundle=create_data_bundle)
        create_response = self._client.CreateDataBundle(
            body=create_request).result()
        data_bundle_id = create_response['data_bundle_id']
        print(data_bundle_id)

        # GetDataBundle
        print("..........Get the Bundle we just created..............")
        get_bundle_response = self._client.GetDataBundle(
            data_bundle_id=data_bundle_id).result()
        data_bundle = get_bundle_response.data_bundle
        print(data_bundle)
        print(data_bundle.id)

        # UpdateDataBundle
        print("..........Update that Bundle.................")
        UpdateDataBundleRequest = self._models.get_model(
            'UpdateDataBundleRequest')
        update_data_bundle = DataBundle(
            name="abc",
            size="12345",
            data_object_ids=[x.id for x in list_response.data_objects],
            checksums=[Checksum(checksum="def", type="md5")],
            aliases=["ghi"])
        update_request = UpdateDataBundleRequest(
            data_bundle_id=data_bundle.id,
            data_bundle=update_data_bundle)
        update_response = self._client.UpdateDataBundle(
            data_bundle_id=data_bundle_id,
            body=update_request).result()
        print("..........Update that Bundle.................")
        updated_bundle = self._client.GetDataBundle(
            data_bundle_id=update_response['data_bundle_id'])\
            .result().data_bundle
        print('updated_bundle.aliases', updated_bundle.aliases)
        print('updated_bundle.updated', updated_bundle.updated)
        print('data_bundle.aliases', data_bundle.aliases)
        print('data_bundle.updated', data_bundle.updated)
        # print(updated_bundle.version)
        # print(updated_bundle.aliases)
        assert updated_bundle.aliases[0] == 'ghi'

        # ListDataBundles
        print("..........List Data Bundles...............")
        ListDataBundlesRequest = self._models.get_model(
            'ListDataBundlesRequest')
        list_request = ListDataBundlesRequest()
        list_response = self._client.ListDataBundles(
            body=list_request).result()
        print(len(list_response.data_bundles))

        # Get all versions of a DataBundle
        print("..........Get all Versions of a Bundle...............")
        versions_response = self._client.GetDataBundleVersions(
            data_bundle_id=data_bundle.id).result()
        print(len(versions_response.data_bundles))

        # Get a DataObject from a bundle
        print("..........Get an Object in a Bundle..............")
        get_bundle_response = self._client.GetDataBundle(
            data_bundle_id=data_bundle_id).result()
        data_bundle = get_bundle_response.data_bundle
        data_object = self._client.GetDataObject(
            data_object_id=data_bundle.data_object_ids[0])\
            .result().data_object
        print(data_object.urls)

        # Get all DataObjects from a bundle
        print("..........Get all Objects in a Bundle..............")
        get_bundle_response = self._client.GetDataBundle(
            data_bundle_id=data_bundle_id).result()
        data_bundle = get_bundle_response.data_bundle
        bundle_objects = []
        for data_object_id in data_bundle.data_object_ids:
            bundle_objects.append(self._client.GetDataObject(
                data_object_id=data_object_id).result().data_object)
        print([x.name for x in bundle_objects])

        # DeleteDataBundle
        print("..........Delete the Bundle...............")
        delete_response = self._client.DeleteDataBundle(
            data_bundle_id=data_bundle_id).result()
        print(delete_response.data_bundle_id)
        try:
            self._client.GetDataBundle(
                data_bundle_id=update_response['data_bundle_id'])\
                .result()
        except Exception as e:
            print('The object no longer exists, '
                  '404 not found. {}'.format(e))

        # Page through a listing of Data Bundles
        print("..........Page through a listing of Data Bundles......")
        for i in range(100):
            my_data_bundle = DataBundle(
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
            body=list_request).result()
        ids = [x['id'] for x in list_response.data_bundles]
        print(list_response.next_page_token)
        print(ids)

        list_request = ListDataBundlesRequest(
            page_size=10, page_token=list_response.next_page_token)
        list_response = self._client.ListDataBundles(
            body=list_request).result()
        ids = [x['id'] for x in list_response.data_bundles]
        print(ids)

        # Find a DataBundle by alias
        print("..........List Data Bundles by alias..............")
        list_request = ListDataBundlesRequest(
            alias=list_response.data_bundles[0].aliases[0])
        alias_list_response = self._client.ListDataBundles(
            body=list_request).result()
        print(list_response.data_bundles[0].aliases[0])
        print(alias_list_response.data_bundles[0].aliases[0])

    def test_no_find(self):
        # this should raise an expected error
        try:
            self._client.GetDataBundle(
                data_bundle_id='NON-EXISTING-KEY').result()
        except HTTPNotFound as e:
            self.assertEquals(e.status_code, 404)
