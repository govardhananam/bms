from django import template

register = template.Library()

@register.filter
def to_replace(value):
    a = str(value)
    return a.replace("+"," ")