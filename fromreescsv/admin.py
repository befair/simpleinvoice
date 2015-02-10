from django.contrib import admin

from fromreescsv.models import Anagrafica, Pagamento

class AnagraficaAdmin(admin.ModelAdmin):

    search_fields = ('name','surname')
    list_filter = ('kind', 'state', 'city')
    list_editable = ('address', 'state', 'city')
    list_display = ('__unicode__', 'kind', 'address', 'state', 'city')
    
class PagamentoAdmin(admin.ModelAdmin):

    list_display = ('date_paid', 'year', 'anagrafica', 'amount')
    search_fields = ('date_paid',)
    list_filter = ('year', 'anagrafica__state', 'anagrafica__city', 'anagrafica__kind')

admin.site.register(Anagrafica, AnagraficaAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
