# Simple client usage via bravo


from bravado.client import SwaggerClient
from bravado.swagger_model import Loader
from bravado.requests_client import RequestsClient

DEFAULT_CONFIG = {
    'validate_requests': False,
    'validate_responses': False
}


class Client:
    """
    simple wrapper around bravado swagger Client. see
    https://github.com/Yelp/bravado/blob/master/docs/source/configuration.rst#client-configuration
    https://github.com/Yelp/bravado#example-with-basic-authentication
    """
    def __init__(self, url, config=DEFAULT_CONFIG, http_client=None):
        swagger_path = '{}/swagger.json'.format(url.rstrip("/"))
        self._config = config
        self.models = SwaggerClient.from_url(swagger_path,
                                             config=config,
                                             http_client=http_client)
        self.client = self.models.DataObjectService

    @classmethod
    def config(cls, url, http_client=None, request_headers=None):
        swagger_path = '{}/swagger.json'.format(url.rstrip("/"))
        http_client = http_client or RequestsClient()
        loader = Loader(http_client, request_headers=request_headers)
        spec_dict = loader.load_spec(swagger_path)
        return spec_dict


def main():
    print('client')


if __name__ == '__main__':
    main()
