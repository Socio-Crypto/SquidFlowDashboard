from django import template

register = template.Library()

@register.filter
def subtract(value, value_2):
    return round(value - value_2)

