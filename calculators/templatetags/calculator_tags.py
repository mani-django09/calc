from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value by the argument."""
    try:
        return int(float(value)) * int(float(arg))
    except (ValueError, TypeError):
        return 0

@register.filter
def format_number(value):
    """Format number with commas."""
    try:
        return f"{int(float(value)):,}"
    except (ValueError, TypeError):
        return value

@register.simple_tag
def multiply(value, multiplier):
    """Simple tag to multiply values"""
    try:
        return int(float(value)) * int(float(multiplier))
    except (ValueError, TypeError):
        return 0