from django import template

register = template.Library()

@register.filter
def cut_email(value):
    a = str(value)
    return a.rpartition('@')[0]