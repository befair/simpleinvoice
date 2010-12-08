
from django import template
from django.template import resolve_variable, loader
from django.template.loader import get_template, select_template

from django.conf import settings
import os.path, base64, datetime

register = template.Library()

#-------------------------------------------------------------------------------
# Filtri

@register.filter
def percent(value):
	return u"%d%%" % (value*100)

