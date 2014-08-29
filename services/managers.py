from django.db import models

class ServiceSubscriptionManager(models.Manager):

    def get_queryset(self):
        """
        Return all ServiceSubscriptions which have not been deleted
        """

        return super(ServiceSubscriptionManager,self).get_queryset().filter(is_deleted=False)
