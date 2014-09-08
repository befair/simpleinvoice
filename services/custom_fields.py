from django import forms
from decimal import Decimal

class PercentageDecimalField(forms.DecimalField):

    def __init__(self, 
        min_value=Decimal('0'), max_value=Decimal('1'), 
        max_digits=3, decimal_places=2,*args, **kwargs 
    ):
        return super(PercentageDecimalField,self).__init__(
            min_value=min_value, max_value=max_value, 
            max_digits=max_digits, decimal_places=decimal_places,
            *args, **kwargs
        )
     
