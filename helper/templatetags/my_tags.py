from django import template
from helper.services.handler import Handler


register = template.Library()


@register.filter
def get_fields(obj):
    return [(field.name, field.value_to_string(obj)) for field in obj._meta.fields]

@register.filter
def remove_character(obj):
    print(str(obj))
    return Handler.delete_character('character', obj)

@register.filter
def get_primary_statistics(obj):
    primaryStatistics = Handler.get_primary_statistics(obj)
    return primaryStatistics.items()

@register.filter
def get_secondary_statistics(obj):
    secondaryStatistics = Handler.get_secondary_statistics(obj)
    return secondaryStatistics.items()

@register.filter
def get_dict(obj):
    di = {}
    for a, b in obj:
        di[a] = b
    return di

