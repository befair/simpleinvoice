
from pprint import pprint
import copy
import requests
import json

from django.conf import settings

API_KEY = settings.FATTURE_IN_CLOUD_API_KEY
API_UID = settings.FATTURE_IN_CLOUD_API_UID
API_ENDPOINT = 'https://api.fattureincloud.it/v1'

def do_request(uri, data={}):
    """All endpoints are accessed through the POST method
    and need API_KEY and API_UID.

    https://secure.fattureincloud.it/api
    """
    url = API_ENDPOINT + uri
    api_data = copy.copy(data)
    api_data.update({
        'api_uid': API_UID,
        'api_key': API_KEY})
    return requests.post(url, json=api_data)


def get_customers(customers=None):
    customers_info = []
    if not customers:
        # retrieve all customers info
        response = do_request('/clienti/lista')
        customers_info = json.loads(response.content)

    return customers_info

def get_invoices(**filters):
    """
    Retrieve invoices details.

    Filter example: {
      "anno": 2017,
      "data_inizio": "01/01/2019",
      "data_fine": "31/12/2019",
      "cliente": "",
      "fornitore": "",
      "id_cliente": "",
      "id_fornitore": "",
      "saldato": "",
      "oggetto": "",
      "ogni_ddt": "",
      "PA": false,
      "PA_tipo_cliente": "",
      "pagina": 1
    }
    """
    response = do_request('/fatture/lista', filters)
    invoices_info = json.loads(response.content)

    return invoices_info

