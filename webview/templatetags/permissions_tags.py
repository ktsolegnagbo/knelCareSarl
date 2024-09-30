
from django import template
from django.contrib.auth.models import User

from webview.models import Employee

register = template.Library()

# @register.simple_tag

webview = 'webview'


@register.filter
def has_permission(user, codename):
    """
    Custom template tag to check if a user has a specific permission.

    Usage:
    {% has_permission user 'app_label.permission_codename' %}
    """
    if isinstance(user, User):
        return user.has_perm(f'{webview}.{codename}')
    return False

#############################

@register.filter
def can_make_payroll(user):
    if isinstance(user, User):
        if user.is_superuser:
            return True
        else:
            appuser = Employee.objects.filter(user=user).first()
            if appuser:
                return appuser.isPayrollUser
    return False

@register.filter
def is_administrator(user):
    if isinstance(user, User):
        if user.is_superuser:
            return True
        else:
            appuser = Employee.objects.filter(user=user).first()
            if appuser:
                return appuser.isAdmin
    return False

@register.filter
def can_give_permission(user):
    if isinstance(user, User):
        if user.is_superuser:
            return True
        else:
            appuser = Employee.objects.filter(user=user).first()
            if appuser:
                return appuser.isAdmin
    return False

@register.filter
def can_see_dashboard(user):
    if isinstance(user, User):
        if user.is_superuser:
            return True
        else:
            appuser = Employee.objects.filter(user=user).first()
            if appuser:
                return appuser.isDashboardUser
    return False

@register.filter
def can_make_print(user):
    if isinstance(user, User):
        if user.is_superuser:
            return True
        else:
            return True
    return False

#############################

@register.filter
def can_create_category(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_category')
    return False

@register.filter
def can_update_category(user):
    if isinstance(user, User):
        return user.has_perm('{webview}.change_category')
    return False

@register.filter
def can_delete_category(user):
    if isinstance(user, User):
        return user.has_perm('{webview}.delete_category')
    return False

@register.filter
def can_view_category(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_category')
    return False

@register.filter
def can_create_client(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_client')
    return False

@register.filter
def can_update_client(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.change_client')
    return False

@register.filter
def can_delete_client(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.delete_client')
    return False

@register.filter
def can_view_client(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_client')
    return False

@register.filter
def can_create_country(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_country')
    return False

@register.filter
def can_update_country(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.change_country')
    return False

@register.filter
def can_delete_country(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.delete_country')
    return False

@register.filter
def can_view_country(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_country')
    return False

@register.filter
def can_create_employee(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_employee')
    return False

@register.filter
def can_update_employee(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.change_employee')
    return False

@register.filter
def can_delete_employee(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.delete_employee')
    return False

@register.filter
def can_view_employee(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_employee')
    return False

@register.filter
def can_create_sale(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_sale')
    return False

@register.filter
def can_update_sale(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.change_sale')
    return False

@register.filter
def can_delete_sale(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.delete_sale')
    return False

@register.filter
def can_view_sale(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_sale')
    return False

@register.filter
def can_create_sale_item(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_sale_item')
    return False

@register.filter
def can_update_sale_item(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.change_sale_item')
    return False

@register.filter
def can_delete_sale_item(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.delete_sale_item')
    return False

@register.filter
def can_view_sale_item(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_sale_item')
    return False

@register.filter
def can_create_payment(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_payment')
    return False

@register.filter
def can_update_payment(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.change_payment')
    return False

@register.filter
def can_delete_payment(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.delete_payment')
    return False

@register.filter
def can_view_payment(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_payment')
    return False

@register.filter
def can_create_payroll(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_payroll')
    return False

@register.filter
def can_update_payroll(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.change_payroll')
    return False

@register.filter
def can_delete_payroll(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.delete_payroll')
    return False

@register.filter
def can_view_payroll(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_payroll')
    return False

@register.filter
def can_create_product(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_product')
    return False

@register.filter
def can_update_product(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.change_product')
    return False

@register.filter
def can_delete_product(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.delete_product')
    return False

@register.filter
def can_view_product(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_product')
    return False

@register.filter
def can_create_role(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_role')
    return False

@register.filter
def can_update_role(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.change_role')
    return False

@register.filter
def can_delete_role(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.delete_role')
    return False

@register.filter
def can_view_role(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_role')
    return False

@register.filter
def can_create_stock(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_stock')
    return False

@register.filter
def can_update_stock(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.change_stock')
    return False

@register.filter
def can_delete_stock(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.delete_stock')
    return False

@register.filter
def can_view_stock(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_stock')
    return False

@register.filter
def can_create_expired_stock(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.add_expired_stock')
    return False

@register.filter
def can_update_expired_stock(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.change_expired_stock')
    return False

@register.filter
def can_delete_expired_stock(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.delete_expired_stock')
    return False

@register.filter
def can_view_expired_stock(user):
    if isinstance(user, User):
        return user.has_perm(f'{webview}.view_expired_stock')
    return False