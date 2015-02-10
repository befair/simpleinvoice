from django.db import models

class Anagrafica(models.Model):

    kind = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    surname = models.CharField(max_length=32, blank=True, null=True)
    rag_soc = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    fax = models.CharField(max_length=32, blank=True, null=True)
    cell = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    skype = models.CharField(max_length=32, blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    zipcode = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    state = models.CharField(max_length=32, blank=True, null=True)
    date_subscription = models.CharField(max_length=32, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_cancelation = models.CharField(max_length=32, blank=True, null=True)

class Pagamento(models.Model):

    anagrafica = models.ForeignKey(Anagrafica)
    surname = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    rag_soc = models.CharField(max_length=256, blank=True, null=True)
    date_paid = models.CharField(max_length=32, blank=True, null=True)


