from django import template

register = template.Library()

@register.simple_tag
def number_of_messages(request):
    return _number
