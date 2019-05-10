from django import template
from everyday.models import *

register = template.Library()

@register.simple_tag
def get_categories():
    return Category.objects.filter(desc = 1).all()