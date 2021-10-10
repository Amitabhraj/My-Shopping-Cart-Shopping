from django import template
from django.template.defaultfilters import stringfilter
from django.forms.fields import CheckboxInput


register = template.Library()

@register.filter(name="sub")
def sub(value, arg):
    return int(value) - int(arg)


@register.filter(name="div")
def sub(value, arg):
    return int(value) / int(arg)


@register.filter(name="mul")
def sub(value, arg):
    return int(value) * int(arg)