from django.shortcuts import get_object_or_404

from webview.utils import givenRate, notEmpty
from .models import AppSite, Country, Product, Employee, Role


def shopping_contents(request):
    shopping_items = []
    totalHT = 0
    product_count = 0
    shopping = request.session.get('shopping', {})
    discount = 0
    discount_type = 'amount'
    discount_amount = 0
    
    
    if request.user.is_authenticated:
        try:
            # Check if a employee exists for the user
            
            # product = Product.objects.get(id=request.user.id)
            # product.delete()
            
            employee, created = Employee.objects.get_or_create(user=request.user)

            if created:
                # Fetch available countries and roles
                countries = Country.objects.all()
                roles = Role.objects.all()

                # Set default country if available
                if countries.exists():
                    employee.country = countries.first()

                # Save the employee to add roles
                employee.save()

                # Add the first available role if roles exist
                if roles.exists():
                    employee.roles.add(roles.first())

                # Set other default employee fields
                employee.email_verified = True
                employee.agree_privacy_policy = True
                employee.save()
            
        except Employee.DoesNotExist:
            # Handle the exception gracefully if something goes wrong
            employee = {}
    else:
        employee = {}

    for item_id, item_data in shopping.items():
        if item_id != 'discount' and item_id != 'discount_type' and not item_id.endswith('_total'):
            product = get_object_or_404(Product, pk=item_id)
            if isinstance(item_data, int):
                totalHT += item_data * product.price
                product_count += item_data
                shopping_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                })
            else:
                for quantity in item_data[''].items():
                    totalHT += quantity * product.price
                    product_count += quantity
                    shopping_items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'product': product,
                    })
        else:
            if item_id == 'discount':
                discount = shopping['discount']
            elif item_id == 'discount_type':
                discount_type = shopping['discount_type']
        
    totalHT = float(totalHT)
    discount = float(discount) if discount else 0.0
    # discount_type = discount_type
    # taxRateBrut = (float(employee.country.tax) if employee.country and employee.country.tax is not None and employee.country.tax > 0 else 0.0)
    # taxRate = (taxRateBrut / 100) if taxRateBrut > 1 else taxRateBrut
    # tax = float(totalHT) * taxRate
    
    try:
        app_site = AppSite.objects.get(site__id=1)
    except Exception:
        app_site = {}
        
        
    if discount_type == 'percent' or discount_type == 'percent_small':
        discount_amount = float(totalHT) * givenRate(discount) if notEmpty(discount) and discount > 0 else 0.0
    else:
        discount_amount = discount if discount and discount >= 0 else 0.0

    
    context = {
        'shopping_items': shopping_items,
        'discount': discount,
        'discount_type': discount_type,
        'discount_amount': discount_amount,
        'totalHT': totalHT,
        'totalGlobalHT': totalHT - discount_amount,
        'product_count': product_count,
        'price_unit': 'FCFA',
        'employee': employee,
        'app_site': app_site
    }
    
    return context
