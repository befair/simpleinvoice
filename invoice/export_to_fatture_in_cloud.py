
from pprint import pprint
import copy
import requests
import json
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from invoice.models import Invoice


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


def get_customers(**filters):
    """
    Retrieve customers info.

    Example filters:
    {
      "filtro": "",
      "id": "",
      "nome": "",
      "cf": "",
      "piva": "",
      "pagina": 1
    }
    """
    response = do_request('/clienti/lista', filters)
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


def get_customer_id(**flt_customer):

    customers = get_customers(**flt_customer)["lista_clienti"]
    if len(customers) == 1:
        id_customer = customers[0]['id']
    elif len(customers) > 1:
        raise MultipleObjectsReturned("troppi clienti %s" % customers)
    else:
        raise ObjectDoesNotExist("cliente non trovato (%s)" % flt_customer)
    return id_customer


def upload_invoice(invoice):
    """
    Upload a SimpleInvoice invoice to FattureInCloud.

    {
      "id_cliente": "0",
      "numero": "1a",
      "data": "19/01/2019",
      "valuta": "EUR",
      "valuta_cambio": 1,
      "prezzi_ivati": false,
      "rivalsa": 0,
      "cassa": 0,
      "rit_acconto": 0,
      "imponibile_ritenuta": 0,
      "rit_altra": 0,
      "marca_bollo": 0,
      "oggetto_visibile": "",
      "oggetto_interno": "",
      "centro_ricavo": "",
      "centro_costo": "",
      "note": "",
      "nascondi_scadenza": false,
      "ddt": false,
      "ftacc": false,
      "id_template": "0",
      "ddt_id_template": "0",
      "ftacc_id_template": "0",
      "mostra_info_pagamento": false,
      "metodo_pagamento": "Bonifico",
      "metodo_titoloN": "IBAN",
      "metodo_descN": "IT01A2345678900000000001234",
      "mostra_totali": "tutti",
      "mostra_bottone_paypal": false,
      "mostra_bottone_bonifico": false,
      "mostra_bottone_notifica": false,
      "lista_articoli": [
        {
          "id": "0",
          "codice": "",
          "nome": "Articolo 1",
          "um": "",
          "quantita": 1,
          "descrizione": "",
          "categoria": "",
          "prezzo_netto": 0,
          "prezzo_lordo": 0,
          "cod_iva": 0,
          "tassabile": true,
          "sconto": 0,
          "applica_ra_contributi": true,
          "ordine": 0,
          "sconto_rosso": 0,
          "in_ddt": false,
          "magazzino": true
        }
      ],
      "lista_pagamenti": [
        {
          "data_scadenza": "19/01/2019",
          "importo": 0,
          "metodo": "not",
          "data_saldo": "19/01/2019"
        }
      ],
      "ddt_numero": "",
      "ddt_data": "19/01/2019",
      "ddt_colli": "",
      "ddt_peso": "",
      "ddt_causale": "",
      "ddt_luogo": "",
      "ddt_trasportatore": "",
      "ddt_annotazioni": "",
      "PA": false,
      "PA_tipo_cliente": "PA",
      "PA_tipo": "nessuno",
      "PA_numero": "",
      "PA_data": "19/01/2019",
      "PA_cup": "",
      "PA_cig": "",
      "PA_codice": "",
      "PA_pec": "",
      "PA_esigibilita": "N",
      "PA_modalita_pagamento": "MP01",
      "PA_istituto_credito": "",
      "PA_iban": "",
      "PA_beneficiario": "",
      "extra_anagrafica": {
        "mail": "info@mariorossi.it",
        "tel": "012345678",
        "fax": "012345678"
      },
      "split_payment": true
    }
    """

    if invoice.discount:
        raise NotImplementedError("Fattura con sconto (=%s) non implementata (pk=%s)" % (invoice.discount, invoice.pk))

    flt_customer = {}
    if invoice.customer.vat:
        flt_customer['piva'] = invoice.customer.vat
    elif invoice.customer.ssn:
        flt_customer['cf'] = invoice.customer.ssn

    try:
        id_customer = get_customer_id(**flt_customer)
    except ObjectDoesNotExist:
        if invoice.customer.vat and invoice.customer.ssn:
            # try again with CF
            id_customer = get_customer_id(**flt_customer)
        else:
            raise

    codici_iva = get_codici_iva()['lista_iva']

    entries_details = []
    for x in invoice.entries.all():

        # Get corresponding codice IVA
        if x.vat_percent == Decimal('0.22'):
            cod_iva = 0
        elif x.vat_percent == Decimal('0.21'):
            cod_iva = 1
        elif x.vat_percent == Decimal('0.2'):
            cod_iva = 2
        else:
            raise NotImplementedError('Per questo valore di IVA (%s) vedere il codice iva con la API /info/account/ {"campi": ["lista_iva"]}' % x.vat_percent)

        # Patch for ",00"
        amount = str(x.amount)
        if amount.endswith(".00"):
            amount = amount[:-3] + ",00"

        entries_details.append({
          "cod_iva": cod_iva,
          "descrizione": x.description,
          "prezzo_netto": amount,
        })

    fields = {
        'id_cliente': id_customer,
        'nome': invoice.customer.name,
        'numero': invoice.real_id,
        'data': invoice.date.strftime("%d/%m/%Y"),
        "mostra_info_pagamento": True,
        "metodo_pagamento": "Bonifico",
        "mostra_bottone_bonifico": True,
        "lista_articoli": entries_details,
        "lista_pagamenti": [{
            "data_scadenza": invoice.date.strftime("%d/%m/%Y"),
            "importo": "auto",
            "metodo": "aziendale",
            "data_saldo": invoice.date.strftime("%d/%m/%Y"),
        }]
    }

    response = do_request('/fatture/nuovo', fields)
    new_invoice = json.loads(response.content)

    return new_invoice

def get_codici_iva():
    data = {"campi": ["lista_iva"]}
    response = do_request('/info/account', data=data)
    return json.loads(response.content)

