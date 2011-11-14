from django.http import HttpResponseBadRequest
from django.contrib.contenttypes.models import ContentType

from django.shortcuts import render_to_response
from django.template import RequestContext

from simpleinvoice.invoice.models import company

def display(request):

    try:
        ct = int(request.GET["ct"])
        ids = request.GET["ids"]
    except KeyError:
        return HttpResponseBadRequest()

    id_list = map(int, ids.split(","))
    model = ContentType.objects.get(pk=ct).model_class()
    qs = model.objects.filter(pk__in=id_list)

    for invoice in qs:
        first_entry = invoice.entries.all()[0]
        if invoice.entries.all().count() != \
            invoice.entries.filter(vat_percent=first_entry.vat_percent).count():

            raise ValueError("Fatture con prodotti a diversa IVA non supportate")

            

    return render_to_response("display_many.html", 
                              { "objs" : qs, "company" : company }, 
                              context_instance=RequestContext(request)
    )
