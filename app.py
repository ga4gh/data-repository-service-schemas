# Simple server implementation

import connexion
from flask_cors import CORS
import uuid

# Our in memory registry
data_objects = {}
data_bundles = {}


def CreateDataObject(**kwargs):
    # Generate a unique identifier
    temp_id = str(uuid.uuid4())
    # TODO Safely create
    data_objects[temp_id] = kwargs['body']
    return({"data_object_id": temp_id}, 200)

def GetDataObject(**kwargs):
    # Get the Data Object from our dictionary
    data_object = data_objects[kwargs['data_object_id']]
    return({"data_object": data_object}, 200)

def UpdateDataObject(**kwargs):
    # Get the Data Object from our dictionary
    data_object = data_objects[kwargs['data_object_id']]
    return(request, 200)

def DeleteDataObject(**kwargs):
    data_object_id = kwargs['data_object_id']
    del data_objects[data_object_id]
    return(kwargs, 204)

def ListDataObjects(**kwargs):
    return(kwargs, 200)

def CreateDataBundle(**kwargs):
    temp_id = str(uuid.uuid4())
    data_bundles[temp_id] = kwargs
    return({"data_bundle_id": temp_id}, 200)

def GetDataBundle(**kwargs):
    data_bundle_id = kwargs['data_bundle_id']
    data_bundle = data_bundles[data_bundle_id]
    return({"data_bundle": data_bundle}, 200)

def UpdateDataBundle(**kwargs):
    data_bundle_id = kwargs['data_bundle_id']
    data_bundle = data_bundles[data_bundle_id]
    return(kwargs, 200)

def DeleteDataBundle(**kwargs):
    data_bundle_id = kwargs['data_bundle_id']
    del data_bundles[data_bundle_id]
    return(kwargs, 204)

def ListDataBundles(**kwargs):
    return(kwargs, 200)

def configure_app():
    # The model name has to match what is in prepare_openapi.sh controller.
    app = connexion.App(
        "app",
        specification_dir='swagger/proto/',
        swagger_ui=True,
        swagger_json=True)

    app.add_api('data_objects_service.swagger.json')

    CORS(app.app)
    return app

if __name__ == '__main__':
    app = configure_app()
    app.run(port=8080,)
