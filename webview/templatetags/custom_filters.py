# templatetags/custom_filters.py
from django import template
from webview.templatetags.functions_extras import to_int

register = template.Library()

@register.filter
def get_data_item(dictionary, key):
    try:
        return dictionary.get(str(key))
    except Exception:
        {}.get(str(key))



@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity



@register.filter(is_safe=True, name="separate_millier")
def separate_millier(n, sep=","):
    """separate data with arg"""
    if n is None or n == "":
        return 0
    s = str(n)
    ll = len(s)
    d = ll/3
    for i in range(1, to_int(d)+1):
        s = s[:ll-3*i] + sep + s[ll-3*i:]
        
    if s.startswith(sep):
        # return s[1:]
        return s.replace(sep, '', 1)
    return s
