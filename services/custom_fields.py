from django.db import models
import decimal

 
class PercentageDecimalField(models.DecimalField):

    def __init__(self, *args, **kwargs ):
        """
        Field to represent percentage values
        """
        
        kwargs['max_digits'] = 3
        kwargs['decimal_places'] = 2
        
        super(PercentageDecimalField,self).__init__(*args, **kwargs)
     
class PyPrettyDecimal(decimal.Decimal):

    def __unicode__(self):
        # TODO: to improve with decimal properties ?!?
        mod = self - int(self)
        if not mod:
            rv = int(self)
        else:
            rv = self.quantize(mod.normalize())
        return unicode(rv)

class PrettyDecimalField(models.DecimalField):

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value is None:
            return value
        try:
            return PyPrettyDecimal(value)
        except decimal.InvalidOperation:
            raise exceptions.ValidationError(self.error_messages['invalid'])


#-----------------------------------------------------------------------------

class CurrencyField(PrettyDecimalField):
    """Subclass of DecimalField.
    It must be positive.

    We do not want to round up to second decimal here.
    We will do it in a place suitable for views.
    """

    def __init__(self, *args, **kw):
        kw['max_digits'] = 10
        kw['decimal_places'] = 4
        super(CurrencyField, self).__init__(*args, **kw)
