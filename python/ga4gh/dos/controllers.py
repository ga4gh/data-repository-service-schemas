import uuid
import datetime
from dateutil.parser import parse


DEFAULT_PAGE_SIZE = 100

# Our in memory registry
data_objects = {}
data_bundles = {}

# Application logic


def now():
    return str(datetime.datetime.now().isoformat("T") + "Z")


def get_most_recent(key):
    max = {'created': '01-01-1965 00:00:00Z'}
    for version in data_objects[key].keys():
        data_object = data_objects[key][version]
        if parse(data_object['created']) > parse(max['created']):
            max = data_object
    return max


# TODO refactor to higher order function
def get_most_recent_bundle(key):
    max = {'created': '01-01-1965 00:00:00Z'}
    for version in data_bundles[key].keys():
        data_bundle = data_bundles[key][version]
        if parse(data_bundle['created']) > parse(max['created']):
            max = data_bundle
    return max


def filter_data_objects(predicate):
    """
    Filters data objects according to a function that acts on each item
    returning either True or False per item.
    """
    return [
        get_most_recent(x[0]) for x in filter(predicate, data_objects.items())]


def filter_data_bundles(predicate):
    """
    Filters data bundles according to a function that acts on each item
    returning either True or False per item.
    """
    return [
        get_most_recent_bundle(x[0]) for x in filter(
            predicate, data_bundles.items())]


def add_created_timestamps(doc):
    """
    Adds created and updated timestamps to the document.
    """
    doc['created'] = now()
    doc['updated'] = now()
    return doc


def add_updated_timestamps(doc):
    """
    Adds created and updated timestamps to the document.
    """
    doc['updated'] = now()
    return doc


stores = {
    'data_objects': data_objects,
    'data_bundles': data_bundles
}


def create(body, key):
    store = stores[key]
    doc = add_created_timestamps(body)
    version = doc.get('version', None)
    if not version:
        doc['version'] = now()
    if doc.get('id', None):
        temp_id = str(uuid.uuid4())
        if store.get(doc['id'], None):
            # issue an identifier if a valid one hasn't been provided
            doc['id'] = temp_id
    else:
        temp_id = str(uuid.uuid4())
        doc['id'] = temp_id
    store[doc['id']] = {}
    store[doc['id']][doc['version']] = doc
    return doc

# Data Object Controllers


def CreateDataObject(**kwargs):
    # TODO Safely create
    body = kwargs['body']['data_object']
    doc = create(body, 'data_objects')
    return({"data_object_id": doc['id']}, 200)


def GetDataObject(**kwargs):
    data_object_id = kwargs['data_object_id']
    version = kwargs.get('version', None)
    # Implementation detail, this server uses integer version numbers.
    # Get the Data Object from our dictionary
    data_object_key = data_objects.get(data_object_id, None)
    if data_object_key and not version:
        data_object = get_most_recent(data_object_id)
        return({"data_object": data_object}, 200)
    elif data_object_key and data_objects[data_object_id].get(version, None):
        data_object = data_objects[data_object_id][version]
        return ({"data_object": data_object}, 200)
    else:
        return("No Content", 404)


def GetDataObjectVersions(**kwargs):
    data_object_id = kwargs['data_object_id']
    # Implementation detail, this server uses integer version numbers.
    # Get the Data Object from our dictionary
    data_object_versions_dict = data_objects.get(data_object_id, None)
    data_object_versions = [x[1] for x in data_object_versions_dict.items()]
    if data_object_versions:
        return({"data_objects": data_object_versions}, 200)
    else:
        return("No Content", 404)


def UpdateDataObject(**kwargs):
    data_object_id = kwargs['data_object_id']
    body = kwargs['body']['data_object']
    # Check to make sure we are updating an existing document.
    old_data_object = get_most_recent(data_object_id)
    # Upsert the new body in place of the old document
    doc = add_updated_timestamps(body)
    doc['created'] = old_data_object['created']
    # We need to safely set the version if they provided one that
    # collides we'll pad it. If they provided a good one, we will
    # accept it. If they don't provide one, we'll give one.
    new_version = doc.get('version', None)
    if new_version and new_version != doc['version']:
        doc['version'] = new_version
    else:
        doc['version'] = now()
    doc['id'] = old_data_object['id']
    data_objects[data_object_id][doc['version']] = doc
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
        selected = get_most_recent(item[0])  # dict.items() gives us a tuple
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
            result_string.append(len(aliases) > 0)
        return False not in result_string
    # Lazy since we're in memory
    filtered = filter_data_objects(filterer)
    page_size = int(body.get('page_size', DEFAULT_PAGE_SIZE))
    # We'll page if there's a provided token or if we have too many
    # objects.
    if len(filtered) > page_size or body.get('page_token', None):
        start_index = int(body.get('page_token', 0)) * page_size
        end_index = start_index + page_size
        # First fill a page
        page = filtered[start_index:min(len(filtered), end_index)]
        if len(filtered[start_index:]) > len(page):
            # If there is more than one page left of results
            next_page_token = int(body.get('page_token', 0)) + 1
            return (
                {"data_objects": page,
                 "next_page_token": str(next_page_token)}, 200)
        else:
            return ({"data_objects": page}, 200)
    else:
        page = filtered
    return({"data_objects": page}, 200)


# Data Bundle Controllers


def CreateDataBundle(**kwargs):
    body = kwargs['body']['data_bundle']
    doc = create(body, 'data_bundles')
    return({"data_bundle_id": doc['id']}, 200)


def GetDataBundle(**kwargs):
    data_bundle_id = kwargs['data_bundle_id']
    version = kwargs.get('version', None)
    # Implementation detail, this server uses integer version numbers.
    # Get the Data Object from our dictionary
    data_bundle_key = data_bundles.get(data_bundle_id, None)
    if data_bundle_key and not version:
        data_bundle = get_most_recent_bundle(data_bundle_id)
        return({"data_bundle": data_bundle}, 200)
    elif data_bundle_key and data_objects[data_bundle_id].get(version, None):
        data_bundle = data_bundles[data_bundle_id][version]
        return ({"data_bundle": data_bundle}, 200)
    else:
        return("No Content", 404)


def UpdateDataBundle(**kwargs):
    data_bundle_id = kwargs['data_bundle_id']
    body = kwargs['body']['data_bundle']
    # Check to make sure we are updating an existing document.
    old_data_bundle = get_most_recent_bundle(data_bundle_id)
    # Upsert the new body in place of the old document
    doc = add_updated_timestamps(body)
    doc['created'] = old_data_bundle['created']
    # We need to safely set the version if they provided one that
    # collides we'll pad it. If they provided a good one, we will
    # accept it. If they don't provide one, we'll give one.
    new_version = old_data_bundle.get('version', None)
    if new_version and new_version != doc.get('version', None):
        doc['version'] = new_version
    else:
        doc['version'] = now()
    doc['id'] = old_data_bundle['id']
    data_bundles[data_bundle_id][doc['version']] = doc
    return({"data_bundle_id": data_bundle_id}, 200)


def GetDataBundleVersions(**kwargs):
    data_bundle_id = kwargs['data_bundle_id']
    data_bundle_versions_dict = data_bundles.get(data_bundle_id, None)
    data_bundle_versions = [x[1] for x in data_bundle_versions_dict.items()]
    if data_bundle_versions:
        return({"data_bundles": data_bundle_versions}, 200)
    else:
        return("No Content", 404)


def DeleteDataBundle(**kwargs):
    data_bundle_id = kwargs['data_bundle_id']
    del data_bundles[data_bundle_id]
    return(kwargs, 200)


def ListDataBundles(**kwargs):
    body = kwargs.get('body')

    def filterer(item):
        """
        This filter is defined as a closure to set gather the kwargs from
        the request. It returns true or false depending on whether to
        include the item in the filter.
        :param item:
        :return: bool
        """
        selected = get_most_recent_bundle(item[0])
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
        if body.get('alias', None):
            aliases = filter(
                lambda x: x == body.get('alias'),
                selected.get('aliases', []))
            result_string.append(len(aliases) > 0)
        return False not in result_string
    # Lazy since we're in memory
    filtered = filter_data_bundles(filterer)
    page_size = int(body.get('page_size', DEFAULT_PAGE_SIZE))
    # We'll page if there's a provided token or if we have too many
    # objects.
    if len(filtered) > page_size or body.get('page_token', None):
        start_index = int(body.get('page_token', 0)) * page_size
        end_index = start_index + page_size
        # First fill a page
        page = filtered[start_index:min(len(filtered), end_index)]
        if len(filtered[start_index:]) > len(page):
            # If there is more than one page left of results
            next_page_token = int(body.get('page_token', 0)) + 1
            return (
                {"data_bundles": page,
                 "next_page_token": str(next_page_token)}, 200)
        else:
            return ({"data_bundles": page}, 200)
    else:
        page = filtered
    return({"data_bundles": page}, 200)
