# -*- coding: utf-8 -*-
import os.path

import swagger_spec_validator.common

cd = os.path.dirname(os.path.realpath(__file__))
SWAGGER_PATH = os.path.join(cd, 'data_object_service.swagger.yaml')


def present_schema():
    """
    Presents the OpenAPI 2.0 schema as a dictionary.
    :rvtype: dict
    """
    return swagger_spec_validator.common.read_file(SWAGGER_PATH)


def from_chalice_routes(routes, base_path=''):
    """
    Given a :obj:`chalice.Chalice.routes` objects, computes the proper
    subset of the Data Object Service schema and presents it as an
    OpenAPI 2.0 JSON schema.
    :rvtype: dict
    :param chalice.Chalice.routes routes:
    :param str base_path: the base path of the endpoints listed in `routes`.
                          This is only necessary if a base path is manually
                          prepended to each endpoint your service exposes,
                          e.g. ``@app.route('/ga4gh/dos/v1/dataobjects')``.
                          This string will be stripped from the beginning of
                          each path in the `routes` object if it is present.
                          The schema will be updated with this value.
    """
    schema = present_schema()

    # Sanitize the routes that are provided so we can compare them easily.
    schema['basePath'] = base_path.rstrip('/').lower() or schema['basePath'].lower()
    sanitized = {}
    for chalice_path, chalice_methods in routes.items():
        path = chalice_path.lower()
        if path.startswith(schema['basePath']):
            path = path.replace(schema['basePath'], '', 1)
        sanitized[path] = [i.lower() for i in chalice_methods]
    routes = sanitized

    # Next, remove from the generated schema paths that are not defined
    # in :obj:`routes`.
    schema['paths'] = {k: v for k, v in schema['paths'].items()
                       if k in routes.keys()}

    # Loop over the remaining paths in the generated schema and remove
    # methods that are not listed in :obj:`routes`.
    for path in schema['paths'].keys():
        schema['paths'][path] = {k: v for k, v in schema['paths'][path].items()
                                 if k in [r.lower() for r in routes[path]]}

    return schema
