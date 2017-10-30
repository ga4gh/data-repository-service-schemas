# Simple client usage via bravo

from bravado.client import SwaggerClient
config = {
    'validate_requests': False,
    'validate_responses': False,
    'host': 'localhost'
}

URL = 'http://localhost:8080'
models = SwaggerClient.from_url('{}/swagger.json'.format(URL), config=config)
client = models.DataObjectService
