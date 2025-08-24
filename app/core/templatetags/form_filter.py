from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    """
    Add CSS class to form field
    Usage: {{ form.field|add_class:"form-control" }}
    """
    return field.as_widget(attrs={'class': css_class})

@register.filter
def get_item(dictionary, key):
    """
    Get item from dictionary
    Usage: {{ dict|get_item:key }}
    """
    return dictionary.get(key)

@register.filter(name='add_attrs')
def add_attrs(field, attrs_string):
    """
    Add multiple attributes to form field
    Usage: {{ form.field|add_attrs:"class:form-control,readonly:true" }}
    """
    attrs = {}
    for attr_pair in attrs_string.split(','):
        if ':' in attr_pair:
            key, value = attr_pair.split(':', 1)
            attrs[key.strip()] = value.strip()
    return field.as_widget(attrs=attrs)

@register.filter(name='field_type')
def field_type(field):
    """
    Get the field widget type
    Usage: {{ form.field|field_type }}
    """
    return field.field.widget.__class__.__name__
