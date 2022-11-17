from django import template
from django.template.defaultfilters import stringfilter
from django.forms.fields import CheckboxInput


register = template.Library()

@register.filter(name="sub")
def sub(value, arg):
    return int(value) - int(arg)

@register.filter(name="index")
def index(value, arg):
    return value[arg-1]


@register.filter(name="div")
def div(value, arg):
    return int(value) / int(arg)


@register.filter(name="mul")
def mul(value, arg):
    return int(value) * int(arg)


@register.filter(name="tax")
def Tax(value, arg):
    tax=int(arg/100*int(value))
    return tax
 

@register.filter(name="net_profit")
def net_profit(value, arg):
    net_profit=int(arg/100*int(value))
    return net_profit


@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

   

