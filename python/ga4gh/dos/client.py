# Simple client usage via bravo

import os

from bravado.client import SwaggerClient
# from bravado.swagger_model import load_file

SWAGGER_FILENAME = 'data_objects_service.swagger.json'
current_directory = os.path.dirname(os.path.realpath(__file__))
SWAGGER_PATH = os.path.join(current_directory, SWAGGER_FILENAME)

DEFAULT_CONFIG = {
    'validate_requests': False,
    'validate_responses': False
}


class Client:
    def __init__(self, url, config=DEFAULT_CONFIG):
        swagger_path = '{}/swagger.json'.format(url.rstrip("/"))
        self._config = config
        self.models = SwaggerClient.from_url(swagger_path, config=config)
        self.client = self.models.DataObjectService


def main():
    print('client')


if __name__ == '__main__':
    main()
