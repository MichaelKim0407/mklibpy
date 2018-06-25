from django import template as _template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

__author__ = 'Michael'

register = _template.Library()


@register.filter(name='markdownify')
def markdownify_filter(value):
    return mark_safe(markdownify(value))
