from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_setting(name):
    """Get a Django setting value"""
    return getattr(settings, name, None)

@register.simple_tag  
def settings_debug():
    """Check if DEBUG is True"""
    return settings.DEBUG