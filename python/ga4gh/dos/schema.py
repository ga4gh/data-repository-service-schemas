# -*- coding: utf-8 -*-
import json
import os.path

import yaml

cd = os.path.dirname(os.path.realpath(__file__))
SWAGGER_PATH = os.path.join(cd, 'data_object_service.swagger.yaml')


def present_schema():
    """
    Presents the OpenAPI 2.0 schema as a dictionary.
    :rvtype: dict
    """
    with open(SWAGGER_PATH, 'r') as schema:
        return yaml.load(schema)


def from_chalice_routes(routes, additions={}):
    """
    Given a :obj:`chalice.Chalice.routes` objects, computes the proper
    subset of the Data Object Service schema and presents it as an
    OpenAPI 2.0 JSON schema.
    :rvtype: str
    :param collections.defaultdict routes: :obj:`chalice.Chalice.routes`
    :param dict additions: a dictionary containing keys to upsert into the schema
    """
    def parse_url(url, base=''):
        """
        Parses a given URL, removing a given basePath (e.g. "/ga4gh/dos/v1")
        if present.
        :param str url: the path to parse, e.g. "/ga4gh/dos/v1/dataobjects"
        :param base: the base path to parse for, e.g. "/ga4gh/dos/v1"
        """
        if url[0:len(base)] == base:
            url = url[len(base):]
        return url

    # Update the generated schema with what the user provides. We do this
    # first because the sanitization step (below) relies on schema['basePath']
    schema = present_schema()
    schema.update(additions)

    # Sanitize the routes that are provided so we can compare them easily.
    sanitized = {}
    for chalice_path, chalice_methods in routes.items():
        path = parse_url(url=chalice_path, base=schema['basePath'])
        sanitized[path] = [i.lower() for i in routes[chalice_path].keys()]
    routes = sanitized

    # Next, remove from the generated schema paths that are not defined
    # in :obj:`routes`.
    schema['paths'] = {k: v for k, v in schema['paths'].items()
                       if k in routes.keys()}

    # Loop over the remaining paths in the generated schema and remove
    # methods that are not listed in :obj:`routes`.
    for path in schema['paths'].keys():
        schema['paths'][path] = {k: v for k, v in schema['paths'][path].items()
                                 if k in routes[path]}

    # Return the generated schema as json
    return json.dumps(schema)
