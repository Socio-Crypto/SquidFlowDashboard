from django import template

register = template.Library()

@register.filter
def subtract(value, value_2):
    return round(value - value_2)

@register.filter
def sum(value, value_2):
    return round(value + value_2)

@register.filter
def shorten_value(value):
    return f"{value[:6]}...{value[-6:]}"

