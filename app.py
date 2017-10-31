# Simple server implementation

import connexion
from flask_cors import CORS

import uuid
import datetime

# Our in memory registry
data_objects = {}
data_bundles = {}

# Application logic


def filter_data_objects(predicate):
    """
    Filters data objects according to a function that acts on each item
    returning either True or False per item.
    """
    return [x[1][0] for x in filter(predicate, data_objects.items())]


def add_created_timestamps(doc):
    """
    Adds created and updated timestamps to the document.
    """
    doc['created'] = str(datetime.datetime.now().isoformat("T") + "Z")
    doc['updated'] = str(datetime.datetime.now().isoformat("T") + "Z")
    return doc


def add_updated_timestamps(doc):
    """
    Adds created and updated timestamps to the document.
    """
    doc['updated'] = str(datetime.datetime.now().isoformat("T") + "Z")
    return doc


# Data Object Controllers


def CreateDataObject(**kwargs):
    # Generate a unique identifier
    temp_id = str(uuid.uuid4())
    # TODO Safely create
    body = kwargs['body']
    doc = add_created_timestamps(body)
    doc['version'] = '0'
    doc['id'] = temp_id
    data_objects[temp_id] = [doc]
    return({"data_object_id": temp_id}, 200)


def GetDataObject(**kwargs):
    data_object_id = kwargs['data_object_id']
    version = kwargs.get('version', '0')
    data_object = None
    # Implementation detail, this server uses integer version numbers.
    # Get the Data Object from our dictionary
    data_object_key = data_objects.get(data_object_id)
    if data_object_key:
        data_object = data_object_key[int(version)]
        return({"data_object": data_object}, 200)
    else:
        return("No Content", 404)


def UpdateDataObject(**kwargs):
    data_object_id = kwargs['data_object_id']
    body = kwargs['body']
    # Check to make sure we are updating an existing document.
    old_data_object = data_objects[data_object_id][0]
    # Upsert the new body in place of the old document
    doc = add_updated_timestamps(body)
    doc['created'] = old_data_object['created']
    # Set the version number to be the length of the array +1, since
    # we're about to append.
    version = str(len(data_objects[data_object_id]))
    doc['version'] = version
    doc['id'] = old_data_object['id']
    data_objects[data_object_id] = [doc] + data_objects[data_object_id]
    return({"data_object_id": data_object_id}, 200)


def DeleteDataObject(**kwargs):
    data_object_id = kwargs['data_object_id']
    del data_objects[data_object_id]
    return({"data_object_id": data_object_id}, 200)


def ListDataObjects(**kwargs):
    body = kwargs.get('body')

    def filterer(item):
        """
        This filter is defined as a closure to set gather the kwargs from
        the request. It returns true or false depending on whether to
        include the item in the filter.
        :param item:
        :return: bool
        """
        selected = item[1][0]  # dict.items() gives us a tuple
        # A list of true and false that all must be true to pass the filter
        result_string = []
        if body.get('checksum', None):
            if body.get('checksum').get('checksum', None):
                sums = filter(
                    lambda x: x == body.get('checksum').get('checksum'),
                    [x['checksum'] for x in selected.get('checksums', [])])
                result_string.append(len(sums) > 0)
            if body.get('checksum').get('type', None):
                types = filter(
                    lambda x: x == body.get('checksum').get('type'),
                    [x['type'] for x in selected.get('checksums', [])])
                result_string.append(len(types) > 0)
        if body.get('url', None):
            urls = filter(
                lambda x: x == body.get('url'),
                [x['url'] for x in selected.get('urls', [])])
            result_string.append(len(urls) > 0)
        if body.get('alias', None):
            aliases = filter(
                lambda x: x == body.get('alias'),
                selected.get('aliases', []))
            print(result_string)
            result_string.append(len(aliases) > 0)
        return False not in result_string
    filtered = filter_data_objects(filterer)
    return({"data_objects": filtered}, 200)


# Data Bundle Controllers


def CreateDataBundle(**kwargs):
    temp_id = str(uuid.uuid4())
    data_bundles[temp_id] = kwargs
    return({"data_bundle_id": temp_id}, 200)


def GetDataBundle(**kwargs):
    data_bundle_id = kwargs['data_bundle_id']
    data_bundle = data_bundles[data_bundle_id]
    return({"data_bundle": data_bundle}, 200)


def UpdateDataBundle(**kwargs):
    # TODO
    # data_bundle_id = kwargs['data_bundle_id']
    # data_bundle = data_bundles[data_bundle_id]
    return(kwargs, 200)


def DeleteDataBundle(**kwargs):
    # TODO
    data_bundle_id = kwargs['data_bundle_id']
    del data_bundles[data_bundle_id]
    return(kwargs, 204)


def ListDataBundles(**kwargs):
    return(kwargs, 200)


def configure_app():
    # The model name has to match what is in
    # tools/prepare_swagger.sh controller.
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
    app.run(port=8080, debug=True)
