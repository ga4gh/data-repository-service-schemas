# With app.py running start this demo, it will load data from GDC public API
# into the service.
import requests

from ga4gh.dos.client import Client

config = {
    'validate_requests': False,
    'validate_responses': False
}

local_client = Client('http://localhost:8080/', config=config)
client = local_client.client
models = local_client.models


GDC_URL = 'https://api.gdc.cancer.gov'

"""
{'data': {'hits': [
{u'data_type': u'Annotated Somatic Mutation',
u'updated_datetime': u'2017-06-17T22:26:30.596775-05:00',
u'created_datetime': u'2017-06-17T19:12:16.993774-05:00',
u'file_name': u'a6c070d8-0619-4c55-b679-0420ace91903.vep.vcf.gz',
u'md5sum': u'd26f933e8b38c5dfba4aa57e47bb4c4c',
u'data_format': u'VCF',
u'submitter_id': u'TCGA-AK-3447-01A-01W-0886-08_TCGA-AK-...',
u'access': u'controlled',
u'state': u'live',
u'file_id': u'ba6c070d8-0619-4c55-b679-0420ace91903',
u'data_category': u'Simple Nucleotide Variation',
u'file_size': 202612,
u'acl': [u'phs000178'],
u'type': u'annotated_somatic_mutation',
u'id': u'a6c070d8-0619-4c55-b679-0420ace91903',
u'file_state': u'submitted',
u'experimental_strategy': u'WXS'}],
u'pagination':
    {u'count': 10,
    u'sort': u'',
    u'from': 350,
    u'pages': 31086,
    u'total': 310858,
    u'page': 36,
    u'size': 10}},
u'warnings': {}}}
"""


def gdc_to_ga4gh(gdc):
    """
    Accepts a gdc dictionary and returns a CreateDataObjectRequest
    :return:
    """
    DataObject = models.get_model('ga4ghDataObject')
    CreateDataObjectRequest = models.get_model('ga4ghCreateDataObjectRequest')
    URL = models.get_model('ga4ghURL')
    Checksum = models.get_model('ga4ghChecksum')
    print(str(gdc.get('file_size')))
    create_data_object = DataObject(
        checksums=[Checksum(checksum=gdc.get('md5sum'), type='md5')],
        name=gdc.get('file_name'),
        size=str(gdc.get('file_size')),
        aliases=[gdc['file_id'], gdc['file_name']],
        urls=[
            URL(
                url="{}/data/{}".format(GDC_URL, gdc.get('file_id')),
                system_metadata=gdc)])
    create_request = CreateDataObjectRequest(data_object=create_data_object)
    return create_request


def post_dos(gdc):
    """
    Takes a GDC hit and indexes it into GA4GH.
    :param gdc:
    :return:
    """
    create_request = gdc_to_ga4gh(gdc)
    create_response = client.CreateDataObject(body=create_request).result()
    return create_response


def load_gdc():
    """
    Gets data from GDC and loads it to DOS.
    :return:
    """
    response = requests.post(
        '{}/files?size=10000&related_files=true'.format(
            GDC_URL), json={}).json()
    hits = response['data']['hits']
    # Initialize to kick off paging
    pagination = {}
    pagination['pages'] = 1
    pagination['page'] = 0
    page_length = 10000
    while int(pagination.get('page')) < int(pagination.get('pages')):
        map(post_dos, hits)
        next_record = pagination.get('page') * page_length
        response = requests.post(
            '{}/files?size=10000&related_files=true&from={}'.format(
                GDC_URL, next_record), json={}).json()
        hits = response['data']['hits']
        pagination = response['data']['pagination']


if __name__ == '__main__':
    load_gdc()
