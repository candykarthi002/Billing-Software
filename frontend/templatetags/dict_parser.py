from django import template

register = template.Library()


@register.filter(name='get')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='values')
def get_item(dictionary):
    return list(dictionary.values())


@register.filter(name='string')
def convert_str(dictionary):
    return str(dictionary)
