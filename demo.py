# With app.py running start this demo
import client

models = client.models
client = client.client

def client_demo():
    # CreateDataObject
    print("..........Create an object............")
    Checksum = models.get_model('ga4ghChecksum')
    CreateDataObjectRequest = models.get_model('ga4ghCreateDataObjectRequest')
    create_request = CreateDataObjectRequest(
        file_name="abc",
        checksum=[Checksum(checksum="def", type=0)],
        urls=["a", "b"])
    create_response = client.CreateDataObject(body=create_request).result()
    data_object_id = create_response['data_object_id']
    print(data_object_id)

    # GetDataObject
    print("..........Get the Object we just created..............")
    data_object = client.GetDataObject(data_object_id=data_object_id).result()
    print(data_object)

    # UpdateDataObject
    print("..........Update that object.................")
    UpdateDataObjectRequest = models.get_model('ga4ghUpdateDataObjectRequest')
    update_request = UpdateDataObjectRequest(
        file_name="abc",
        checksum=[Checksum(checksum="def", type=0)],
        urls=["a", "b", "c"])
    update_response = client.UpdateDataObject(
        data_object_id=data_object_id, body=update_request).result()
    updated_object = client.GetDataObject(
        data_object_id=update_response['data_object_id']).result()
    print(updated_object)

    # ListDataObjects

    # DeleteDataObject
    print("..........Delete the Object...............")
    delete_response = client.DeleteDataObject(
        data_object_id=data_object_id).result()
    print(delete_response)
    try:
        deleted_object = client.GetDataObject(
            data_object_id=update_response['data_object_id']).result()
    except Exception as e:
        print("The object no longer exists, 404 not found.")

    # CreateDataBundle

    # GetDataBundle

    # UpdateDataBundle

    # ListDataBundles

    # DeleteDataBundle

if __name__ == '__main__':
    client_demo()
