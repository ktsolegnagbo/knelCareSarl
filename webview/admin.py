from django.contrib import admin
from .models import AppSite, Category, Client, ExpiredStock, Sale, SaleItem, Payment, Payroll, Product, Country, Employee, Role, Stock

class AppSiteAdmin(admin.ModelAdmin):
    list_display = (
        'site',
        'email',
        'owner_email',
        'phone_number',
        'phone_number_other',
        'address',
        'info',
        'recip',
    )
    
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tax',
    )

class RoleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
    )
    
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'salary_brut',
        'position',
        'phone_number',
        # 'country',
        'employee_pic',
        'employee_pic_thumb',
        'biography',
        'location',
        'birth_date',
        'email_verified',
        'agree_privacy_policy',
        'list_roles'
    )
    
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'phone_number_other',
        'address',
        'country',
        'city',
        'loyalty_point'
    )
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'category',
        'name',
        'price',
        'alert_threshold',
        'description',
        'is_available',
        'image_url',
        'image',
        'deleted',
    )
    # ordering = ('name',)

class StockAdmin(admin.ModelAdmin):
    list_display = (
        # 'id',
        'user',
        'product',
        'price',
        'quantity',
        'amount',
        'expiration_date',
    )

class ExpiredStockAdmin(admin.ModelAdmin):
    list_display = (
        # 'id',
        'user',
        'product',
        'quantity',
        'expiration_date',
    )

class SaleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order_number',
        'user',
        'client',
        'discount',
        'tax_rate',
        'ht_amount',
        'payment_due_date',
    )
    # list_filter = ['status', 'date']
    # search_fields = ['client__name']

class SaleItemAdmin(admin.ModelAdmin):
    list_display = (
        'sale',
        'product',
        'quantity',
        'price',
    )
class PayrollAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'date',
        'salary_brut',
        'cnss',
        'irpp',
        'other_deductions',
        'commission',
        'salary_net',
        'deleted'
    )

admin.site.register(AppSite, AppSiteAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(ExpiredStock, ExpiredStockAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem, SaleItemAdmin)
admin.site.register(Payroll, PayrollAdmin)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'sale', 'amount', 'date', 'method', 'status']
    list_filter = ['method', 'date', 'status']
        
# @admin.register(LoyaltyHistory)
# class LoyaltyHistoryAdmin(admin.ModelAdmin):
#     list_display = ['client', 'points_earned', 'points_spent', 'date']
#     list_filter = ['date']

