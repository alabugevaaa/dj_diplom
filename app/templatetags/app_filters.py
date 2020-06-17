from django import template


register = template.Library()


@register.filter
def star(value):
    return '★' * value


