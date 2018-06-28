# -*- coding: utf-8 -*-
"""
This module exposes a single class :class:`ga4gh.dos.client.Client`, which
exposes the HTTP methods of the Data Object Service as named Python functions.

This makes it easy to access resources that are described following these
schemas, and uses bravado to dynamically generate the client functions
following the OpenAPI schema.

It currently assumes that the service also hosts the swagger.json, in a style
similar to the demonstration server, :mod:`ga4gh.dos.server`.
"""
from bravado.client import SwaggerClient
from bravado.swagger_model import Loader
from bravado.requests_client import RequestsClient
from bravado_core.exception import SwaggerValidationError
from bravado_core.formatter import SwaggerFormat

DEFAULT_CONFIG = {
    'validate_requests': True,
    'validate_responses': True
}


def validate_int64(test):
    """
    Accepts an int64 and checks for numerality. Throws a Swagger Validation
    exception when failing the test.

    :param test:
    :return:
    :raises SwaggerValidationError:
    """
    if str(test) != test:
        raise SwaggerValidationError('int64 are serialized as strings')


# This is to support serializing int64 as strings on the wire. JavaScript
# only supports up to 2^53.
int64_format = SwaggerFormat(
    format='int64',
    to_wire=lambda i: str(i),
    to_python=lambda i: int(i),
    validate=validate_int64,  # jsonschema validates integer
    description="Converts [wire]str:int64 <=> python long"
)


class Client:
    """
    This class is the instantiated to create a new connection to a DOS. It
    connects to the service to download the swagger.json and returns a client
    in the DataObjectService namespace.

    ::

        from ga4gh.dos.client import Client
        client = Client("http://localhost:8000/ga4gh/dos/v1")

        models = client.models
        c = client.client

        # Will return a Data Object by identifier
        c.GetDataObject(data_object_id="abc").result()

        # To access models in the Data Object Service namespace:
        ListDataObjectRequest = models.get_model('ListDataObjectsRequest')

        # And then instantiate a request with our own query:
        my_request = ListDataObjectsRequest(alias="doi:10.0.1.1/1234")

        # Finally, send the request to the service and evaluate the response.
        c.ListDataObjects(body=my_request).result()


    The class accepts a configuration dictionary that maps directly to the
    bravado configuration.

    For more information on configuring the client, see
    `bravado documentation
    <https://github.com/Yelp/bravado/blob/master/docs/source/configuration.rst>`_.
    """
    def __init__(self, url, config=DEFAULT_CONFIG, http_client=None, request_headers=None):
        swagger_path = '{}/swagger.json'.format(url.rstrip("/"))
        config['formats'] = [int64_format]
        self._config = config
        self.models = SwaggerClient.from_url(swagger_path,
                                             config=config,
                                             http_client=http_client,
                                             request_headers=request_headers)
        self.client = self.models.DataObjectService

    @classmethod
    def config(cls, url, http_client=None, request_headers=None):
        """
        Accepts an optionally configured requests client with authentication
        details set.

        :param url: The URL of the service to connect to
        :param http_client: The http_client to use, \
          defaults to :func:`RequestsClient`
        :param request_headers: The headers to set on each request.
        :return:
        """
        swagger_path = '{}/swagger.json'.format(url.rstrip('/'))
        http_client = http_client or RequestsClient()
        loader = Loader(http_client, request_headers=request_headers)
        spec_dict = loader.load_spec(swagger_path)
        return spec_dict


def main():
    print('client')


if __name__ == '__main__':
    main()
