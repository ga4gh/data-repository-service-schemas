# With app.py running start this demo
import client

models = client.models
client = client.client


def client_demo():
    # CreateDataObject
    print("..........Create an object............")
    Checksum = models.get_model('ga4ghChecksum')
    URL = models.get_model('ga4ghURL')
    CreateDataObjectRequest = models.get_model('ga4ghCreateDataObjectRequest')
    DataObject = models.get_model('ga4ghCreateDataObjectRequest')
    create_data_object = DataObject(
        file_name="abc",
        checksums=[Checksum(checksum="def", type="md5")],
        urls=[URL(url="a"), URL(url="b")])
    create_request = CreateDataObjectRequest(data_object=create_data_object)
    create_response = client.CreateDataObject(body=create_request).result()
    data_object_id = create_response['data_object_id']
    print(data_object_id)

    # GetDataObject
    print("..........Get the Object we just created..............")
    get_object_response = client.GetDataObject(
        data_object_id=data_object_id).result()
    data_object = get_object_response.data_object
    print(data_object.id)

    # UpdateDataObject
    print("..........Update that object.................")
    UpdateDataObjectRequest = models.get_model('ga4ghUpdateDataObjectRequest')
    update_data_object = DataObject(
        file_name="abc",
        checksums=[Checksum(checksum="def", type="md5")],
        urls=[URL(url="a"), URL(url="b"), URL(url="c")])
    update_request = UpdateDataObjectRequest(data_object=update_data_object)
    update_response = client.UpdateDataObject(
        data_object_id=data_object_id, body=update_request).result()
    updated_object = client.GetDataObject(
        data_object_id=update_response['data_object_id']).result().data_object
    print(updated_object.version)

    # Get the old DataObject
    print("..........Get the old Data Object.................")
    old_data_object = client.GetDataObject(
        data_object_id=update_response['data_object_id'],
        version=data_object.version).result().data_object
    print(old_data_object.version)

    # ListDataObjects
    print("..........List Data Objects...............")
    ListDataObjectsRequest = models.get_model('ga4ghListDataObjectsRequest')
    list_request = ListDataObjectsRequest()
    list_response = client.ListDataObjects(body=list_request).result()
    print(len(list_response.data_objects))

    # Get all versions of a DataObject
    print("..........Get all Versions...............")
    versions_response = client.GetDataObjectVersions(
        data_object_id=old_data_object.id).result()
    print(len(versions_response.data_objects))

    # DeleteDataObject
    print("..........Delete the Object...............")
    delete_response = client.DeleteDataObject(
        data_object_id=data_object_id).result()
    print(delete_response.data_object_id)
    try:
        client.GetDataObject(
            data_object_id=update_response['data_object_id']).result()
    except Exception as e:
        print('The object no longer exists, 404 not found. {}'.format(e))

    # Create a Data Object specifying your own version
    print(".......Create a Data Object with our own version..........")
    my_data_object = DataObject(
        file_name="abc",
        checksums=[Checksum(checksum="def", type="md5")],
        urls=[URL(url="a"), URL(url="b")],
        version="great-version")
    create_request = CreateDataObjectRequest(data_object=my_data_object)
    create_response = client.CreateDataObject(body=create_request).result()
    data_object_id = create_response['data_object_id']
    data_object = client.GetDataObject(
        data_object_id=data_object_id).result().data_object
    print(data_object.version)

    # Create a Data Object specifying your own ID
    print("..........Create a Data Object with our own ID..............")
    my_data_object = DataObject(
        id="myid",
        file_name="abc",
        checksums=[Checksum(checksum="def", type="md5")],
        urls=[URL(url="a"), URL(url="b")])
    create_request = CreateDataObjectRequest(data_object=my_data_object)
    create_response = client.CreateDataObject(body=create_request).result()
    data_object_id = create_response['data_object_id']
    print(data_object_id)

    # Page through a listing of data objects
    print("..........Page through a listing of Objects..............")
    for i in range(100):
        my_data_object = DataObject(
            file_name="abc",
            checksums=[Checksum(checksum="def", type="md5")],
            urls=[URL(url="a")])
        create_request = CreateDataObjectRequest(data_object=my_data_object)
        client.CreateDataObject(body=create_request).result()
    list_request = ListDataObjectsRequest(page_size=10)
    list_response = client.ListDataObjects(body=list_request).result()
    ids = [x.id for x in list_response.data_objects]
    print(list_response.next_page_token)
    print(ids)

    list_request = ListDataObjectsRequest(
        page_size=10, page_token=list_response.next_page_token)
    list_response = client.ListDataObjects(body=list_request).result()
    ids = [x.id for x in list_response.data_objects]
    print(ids)

    # CreateDataBundle

    # GetDataBundle

    # UpdateDataBundle

    # ListDataBundles

    # DeleteDataBundle


if __name__ == '__main__':
    client_demo()
