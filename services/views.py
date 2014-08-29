from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

from services.models import ServiceSubscription, Service
from invoice.models import Customer

import json

# API -----

@staff_member_required
def get_services(request, customer_id):
    """
    API view.
    Returns all services and subscriptions of a given Customer in JSON.

    """
    
    response = {}

    customer = get_object_or_404(Customer, pk=customer_id)

    for sub in ServiceSubscription.objects.filter(customer=customer):
        response[sub.service.id] = {
            'service_id': sub.service.id,
            'service_name': sub.service.name,
            'amount': str(sub.service.amount),
            'vat': str(sub.vat_percent),
            'discount': str(sub.discount),
        }
    
    return HttpResponse(
        json.dumps(response),
        content_type="application/json"
    )
