# -*- coding: utf-8 -*-
"""
Data Repository Service Controller Functions

These controller functions for the demo server implement an opinionated version
of DRS by providing uuid's to newly create objects, and using timestamp
versions.

Initializes an in-memory dictionary for storing Objects.
"""
import uuid
import datetime
from dateutil.parser import parse


DEFAULT_PAGE_SIZE = 100

# Our in memory registry
objects = {}
bundles = {}

# Application logic


def now():
    """
    Returns the current time in string format.
    :return: Current ISO time.
    """
    return str(datetime.datetime.now().isoformat("T") + "Z")


def get_most_recent(key):
    """
    Gets the most recent Object for a key.
    :param key:
    :return:
    """
    max = {'updated': '01-01-1965 00:00:00Z'}
    if key not in objects:
        raise KeyError("object not found!")
    for version in objects[key].keys():
        object = objects[key][version]
        if parse(object['updated']) > parse(max['updated']):
            max = object
    return max


# TODO refactor to higher order function
def get_most_recent_bundle(key):
    """
    Returns the most recent bundle for the given key.

    :param key:
    :return:
    """
    max = {'updated': '01-01-1965 00:00:00Z'}
    for version in bundles[key].keys():
        bundle = bundles[key][version]
        if parse(bundle['updated']) > parse(max['updated']):
            max = bundle
    return max


def filter_objects(predicate):
    """
    Filters data objects according to a function that acts on each item
    returning either True or False per item.
    """
    return [get_most_recent(x[0]) for x in filter(predicate, objects.items())]


def filter_bundles(predicate):
    """
    Filters data bundles according to a function that acts on each item
    returning either True or False per item.
    :param predicate: A function used to test items
    :return: List of Data Bundles
    """
    return [
        get_most_recent_bundle(x[0]) for x in filter(
            predicate, bundles.items())]


def add_created_timestamps(doc):
    """
    Adds created and updated timestamps to the document.
    :param doc: A document to be timestamped
    :return doc: The timestamped document
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
    'objects': objects,
    'bundles': bundles
}


def create(body, key):
    """
    Creates a new document at the given key by adding necessary metadata
    and storing in the in-memory store.
    :param body:
    :param key:
    :return:
    """
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


def CreateObject(**kwargs):
    """
    Creates a new Data Object by issuing an identifier if it is not
    provided.

    :param kwargs:
    :return:
    """
    # TODO Safely create
    body = kwargs['body']['object']
    doc = create(body, 'objects')
    return({"object_id": doc['id']}, 200)


def GetObject(**kwargs):
    """
    Get a Data Object by object_id.
    :param kwargs:
    :return:
    """
    object_id = kwargs['object_id']
    version = kwargs.get('version', None)
    # Implementation detail, this server uses integer version numbers.
    # Get the Data Object from our dictionary
    object_key = objects.get(object_id, None)
    if object_key and not version:
        object = get_most_recent(object_id)
        return({"object": object}, 200)
    elif object_key and objects[object_id].get(version, None):
        object = objects[object_id][version]
        return ({"object": object}, 200)
    else:
        return({'msg': "The requested Data "
                       "Object wasn't found", 'status_code': 404}, 404)


def GetObjectVersions(**kwargs):
    """
    Returns all versions of a Data Object.
    :param kwargs:
    :return:
    """
    object_id = kwargs['object_id']
    # Implementation detail, this server uses integer version numbers.
    # Get the Data Object from our dictionary
    object_versions_dict = objects.get(object_id, None)
    object_versions = [x[1] for x in object_versions_dict.items()]
    if object_versions:
        return({"objects": object_versions}, 200)
    else:
        return({'msg': "The requested Data "
                       "Object wasn't found", 'status_code': 404}, 404)


def UpdateObject(**kwargs):
    """
    Update a Data Object by creating a new version.

    :param kwargs:
    :return:
    """
    object_id = kwargs['object_id']
    body = kwargs['body']['object']
    # Check to make sure we are updating an existing document.
    try:
        old_object = get_most_recent(object_id)
    except KeyError:
        return "Data object not found", 404
    # Upsert the new body in place of the old document
    doc = add_updated_timestamps(body)
    doc['created'] = old_object['created']
    # We need to safely set the version if they provided one that
    # collides we'll pad it. If they provided a good one, we will
    # accept it. If they don't provide one, we'll give one.
    new_version = doc.get('version', None)
    if not new_version or new_version in objects[object_id].keys():
        doc['version'] = now()
    doc['id'] = old_object['id']
    objects[object_id][doc['version']] = doc
    return({"object_id": object_id}, 200)


def DeleteObject(**kwargs):
    """
    Delete a Data Object by object_id.

    :param kwargs:
    :return:
    """
    object_id = kwargs['object_id']
    del objects[object_id]
    return({"object_id": object_id}, 200)


def ListObjects(**kwargs):
    """
    Returns a list of Data Objects matching a ListObjectsRequest.

    :param kwargs: alias, url, checksum, checksum_type, page_size, page_token
    :return:
    """
    def filterer(item):
        """
        This filter is defined as a closure to set gather the kwargs from
        the request. It returns true or false depending on whether to
        include the item in the filter.
        :param item:
        :return: bool
        """
        selected = get_most_recent(item[0])  # dict.items() gives us a tuple
        sel_checksum = selected.get('checksums', [])

        if kwargs.get('checksum', None):
            if kwargs['checksum'] not in [i['checksum'] for i in sel_checksum]:
                return False
        if kwargs.get('checksum_type', None):
            if kwargs['checksum_type'] not in [i['type'] for i in sel_checksum]:
                return False
        if kwargs.get('url', None):
            if kwargs['url'] not in [i['url'] for i in selected.get('urls', [])]:
                return False
        if kwargs.get('alias', None):
            if kwargs['alias'] not in selected.get('aliases', []):
                return False
        return True

    # Lazy since we're in memory
    filtered = filter_objects(filterer)
    page_size = int(kwargs.get('page_size', DEFAULT_PAGE_SIZE))
    # We'll page if there's a provided token or if we have too many
    # objects.
    if len(filtered) > page_size or kwargs.get('page_token', None):
        start_index = int(kwargs.get('page_token', 0)) * page_size
        end_index = start_index + page_size
        # First fill a page
        page = filtered[start_index:min(len(filtered), end_index)]
        if len(filtered[start_index:]) - len(page) > 0:
            # If there is more than one page left of results
            next_page_token = int(kwargs.get('page_token', 0)) + 1
            return (
                {"objects": page,
                 "next_page_token": str(next_page_token)}, 200)
        else:
            return ({"objects": page}, 200)
    else:
        page = filtered
    return({"objects": page}, 200)


# Data Bundle Controllers


def CreateBundle(**kwargs):
    """
    Create a Data Bundle, issuing a new identifier if one is not provided.

    :param kwargs:
    :return:
    """
    body = kwargs['body']['bundle']
    doc = create(body, 'bundles')
    return({"bundle_id": doc['id']}, 200)


def GetBundle(**kwargs):
    """
    Get a Data Bundle by identifier.

    :param kwargs:
    :return:
    """
    bundle_id = kwargs['bundle_id']
    version = kwargs.get('version', None)
    # Implementation detail, this server uses integer version numbers.
    # Get the Data Object from our dictionary
    bundle_key = bundles.get(bundle_id, None)
    if bundle_key and not version:
        bundle = get_most_recent_bundle(bundle_id)
        return({"bundle": bundle}, 200)
    elif bundle_key and objects[bundle_id].get(version, None):
        bundle = bundles[bundle_id][version]
        return ({"bundle": bundle}, 200)
    else:
        return({'msg': "The requested Data "
                       "Bundle wasn't found", 'status_code': 404}, 404)


def UpdateBundle(**kwargs):
    """
    Updates a Data Bundle to include new metadata by upserting the new
    bundle.

    :param kwargs:
    :return:
    """
    bundle_id = kwargs['bundle_id']
    body = kwargs['body']['bundle']
    # Check to make sure we are updating an existing document.
    old_bundle = get_most_recent_bundle(bundle_id)
    # Upsert the new body in place of the old document
    doc = add_updated_timestamps(body)
    doc['created'] = old_bundle['created']
    # We need to safely set the version if they provided one that
    # collides we'll pad it. If they provided a good one, we will
    # accept it. If they don't provide one, we'll give one.
    new_version = doc.get('version', None)
    if not new_version or new_version in bundles[bundle_id].keys():
        doc['version'] = now()
    doc['id'] = old_bundle['id']
    bundles[bundle_id][doc['version']] = doc
    return({"bundle_id": bundle_id}, 200)


def GetBundleVersions(**kwargs):
    """
    Get all versions of a Data Bundle.

    :param kwargs:
    :return:
    """
    bundle_id = kwargs['bundle_id']
    bundle_versions_dict = bundles.get(bundle_id, None)
    bundle_versions = [x[1] for x in bundle_versions_dict.items()]
    if bundle_versions:
        return({"bundles": bundle_versions}, 200)
    else:
        return({'msg': "The requested Data "
                       "Bundle wasn't found", 'status_code': 404}, 404)


def DeleteBundle(**kwargs):
    """
    Deletes a Data Bundle by ID.

    :param kwargs:
    :return:
    """
    bundle_id = kwargs['bundle_id']
    del bundles[bundle_id]
    return(kwargs, 200)


def ListBundles(**kwargs):
    """
    Takes a ListBundles request and returns the bundles that match
    that request. Possible kwargs: alias, url, checksum, checksum_type, page_size, page_token

    :param kwargs: ListBundles request.
    :return:
    """
    def filterer(item):
        """
        This filter is defined as a closure to set gather the kwargs from
        the request. It returns true or false depending on whether to
        include the item in the filter.
        :param item:
        :rtype: bool
        """
        selected = get_most_recent_bundle(item[0])
        sel_checksum = selected.get('checksums', [])
        if kwargs.get('checksum', None):
            if kwargs['checksum'] not in [i['checksum'] for i in sel_checksum]:
                return False
        if kwargs.get('checksum_type', None):
            if kwargs['checksum_type'] not in [i['type'] for i in sel_checksum]:
                return False
        if kwargs.get('alias', None):
            if kwargs['alias'] not in selected.get('aliases', []):
                return False
        return True
    # Lazy since we're in memory
    filtered = filter_bundles(filterer)
    page_size = int(kwargs.get('page_size', DEFAULT_PAGE_SIZE))
    # We'll page if there's a provided token or if we have too many
    # objects.
    if len(filtered) > page_size:
        start_index = int(kwargs.get('page_token', 0)) * page_size
        end_index = start_index + page_size
        # First fill a page
        page = filtered[start_index:min(len(filtered), end_index)]
        if len(filtered[start_index:]) - len(page) > 0:
            # If there is more than one page left of results
            next_page_token = int(kwargs.get('page_token', 0)) + 1
            return (
                {"bundles": page,
                 "next_page_token": str(next_page_token)}, 200)
        else:
            return ({"bundles": page}, 200)
    else:
        page = filtered
    return({"bundles": page}, 200)


def GetServiceInfo(**kwargs):
    import ga4gh.drs.schema
    return ga4gh.drs.schema.present_schema()['info'], 200
