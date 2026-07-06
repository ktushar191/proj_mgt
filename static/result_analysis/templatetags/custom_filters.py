# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def is_in_list(value, my_list):
    """Check if value is in the provided list."""
    return value in my_list

@register.filter
def get_item(dictionary, key):
    """Return the value for key from the dictionary, or None if the key doesn't exist."""
    return dictionary.get(key)