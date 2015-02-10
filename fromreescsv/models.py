#-*- coding: utf-8 -*-
from django.db import models

class Anagrafica(models.Model):

    kind = models.CharField(max_length=32, blank=True, null=True, verbose_name="tipo")
    name = models.CharField(max_length=32, blank=True, null=True)
    surname = models.CharField(max_length=32, blank=True, null=True)
    rag_soc = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name="telefono")
    fax = models.CharField(max_length=32, blank=True, null=True)
    cell = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    skype = models.CharField(max_length=32, blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True, verbose_name="indirizzo")
    zipcode = models.CharField(max_length=32, blank=True, null=True, verbose_name="cap")
    city = models.CharField(max_length=32, blank=True, null=True, verbose_name="città")
    state = models.CharField(max_length=32, blank=True, null=True, verbose_name="prov")
    date_subscription = models.CharField(max_length=32, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_cancelation = models.CharField(max_length=32, blank=True, null=True)

    def __unicode__(self):
        return u"%s %s (%s)" % (self.name, self.surname, self.rag_soc)

class Pagamento(models.Model):

    anagrafica = models.ForeignKey(Anagrafica)
    #surname = models.CharField(max_length=32, blank=True, null=True)
    #name = models.CharField(max_length=32, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True, verbose_name="importo")
    year = models.IntegerField(blank=True, null=True, verbose_name="anno")
    #rag_soc = models.CharField(max_length=256, blank=True, null=True)
    date_paid = models.CharField(max_length=32, blank=True, null=True, verbose_name="data pag")

    def __unicode__(self):
        return "Quota %s -> %s" % (self.year, self.anagrafica)


