# Simple client usage via bravo

from bravado.client import SwaggerClient
config = {
    'validate_requests': False,
    'validate_responses': False,
    'host': 'localhost'
}

models = SwaggerClient.from_url('http://localhost:8080/swagger.json')
client = models.DataObjectService
