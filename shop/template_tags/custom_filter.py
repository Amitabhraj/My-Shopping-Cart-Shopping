from django import template
from django.template.defaultfilters import stringfilter
from django.forms.fields import CheckboxInput


register = template.Library()

@register.filter(name="sub")
def sub(value, arg):
    return int(value) - int(arg)


@register.filter(name="div")
def div(value, arg):
    return int(value) / int(arg)


@register.filter(name="mul")
def mul(value, arg):
    return int(value) * int(arg)


@register.filter(name="tax")
def Tax(value, arg):
    net_profit_on_1_product=int(value) * int(arg)
    tax=int(5/100*int(net_profit_on_1_product))
    return tax
 

@register.filter(name="net_profit")
def net_profit(value, arg):
    net_profit_on_1_product=int(value) * int(arg)
    tax=5/100*int(net_profit_on_1_product)
    splited_tax=str(tax).split('.')
    net_tax=int(splited_tax[0])
    return int(net_profit_on_1_product) - (net_tax)


@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

   

