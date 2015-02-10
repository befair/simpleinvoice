from django.contrib import admin

from fromreescsv.models import Anagrafica, Pagamento

class AnagraficaAdmin(admin.ModelAdmin):

    search_fields = ('name','surname')
    list_filter = ('kind', 'state', 'city')
    list_filter = ('kind', 'address', 'name', 'surname', 'state', 'city')
    list_display = ('name', 'surname', 'rag_soc', 'address', 'state', 'city')
    
class PagamentoAdmin(admin.ModelAdmin):

    list_display = ('anagrafica__name', 'anagrafica__surname', 'amount', 'date_paid')

admin.site.register(Anagrafica, AnagraficaAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
