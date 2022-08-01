
from django import template

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter(name='split')
def split(value, key):
    res = value.split(key)
    if value[-1] != key:
        return res
    res.pop()
    return res
