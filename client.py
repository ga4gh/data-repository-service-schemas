# Simple client usage via bravo

from bravado.client import SwaggerClient
config = {
    'validate_requests': False,
    'validate_responses': False,
    'host': 'localhost'
}
models = SwaggerClient.from_url('http://localhost:8080/swagger.json')
client = models.DataObjectService

# CreateDataObject
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
data_object = client.GetDataObject(data_object_id=data_object_id).result()
print(data_object)

# UpdateDataObject

# ListDataObjects

# DeleteDataObject

# CreateDataBundle

# GetDataBundle

# UpdateDataBundle

# ListDataBundles

# DeleteDataBundle
