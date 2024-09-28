from .views import GroupListView, GroupCreateView, GroupUpdateView, GroupDeleteView
from django.urls import path

from . import views

# app_name = 'webview'

urlpatterns = [
    path('', views.home, name='home'),
    path('update_app_site/', views.update_app_site, name='update_app_site'),
    
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('activation/<uidb64>/<token>/', views.activate_email, name='activate_email'),
    
    path('products/', views.all_products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/details/', views.get_product_details, name='get_product_details'),
    
    path('admin-products/', views.admin_products, name='admin_list_products'),
    path('admin-products/create/', views.admin_products, name='admin_create_product'),
    path('admin-products/update/<int:product_id>/', views.admin_products, name='admin_update_product'),
    path('admin-products/delete/<int:product_id>/', views.admin_products, name='admin_delete_product'),
    
    path('admin-clients/', views.admin_clients, name='admin_list_clients'),
    path('admin-clients/create/', views.admin_clients, name='admin_create_client'),
    path('admin-clients/update/<int:client_id>/', views.admin_clients, name='admin_update_client'),
    path('admin-clients/delete/<int:client_id>/', views.admin_clients, name='admin_delete_client'),
    path('admin-clients/details/<int:client_id>/', views.admin_clients_details, name='admin_clients_details'),
    
    path('admin-stocks/', views.admin_stocks, name='admin_list_stocks'),
    path('admin-stocks/create/', views.admin_stocks, name='admin_create_stock'),
    path('admin-stocks/update/<int:stock_id>/', views.admin_stocks, name='admin_update_stock'),
    path('admin-stocks/delete/<int:stock_id>/', views.admin_stocks, name='admin_delete_stock'),
    
    path('admin-categories/', views.admin_categories, name='admin_list_categories'),
    path('admin-categories/create/', views.admin_categories, name='admin_create_category'),
    path('admin-categories/update/<int:category_id>/', views.admin_categories, name='admin_update_category'),
    path('admin-categories/delete/<int:category_id>/', views.admin_categories, name='admin_delete_category'),
    
    path('admin-users/', views.admin_users, name='admin_list_users'),
    path('admin-users/create/', views.admin_users, name='admin_create_user'),
    path('admin-users/update/<int:user_id>/', views.admin_users, name='admin_update_user'),
    path('admin-users/delete/<int:user_id>/', views.admin_users, name='admin_delete_user'),
    path('admin-users/salary-payment/<int:user_id>/', views.admin_users, name='admin_employee_salary_payment'),
    
    path('admin-payrolls/', views.admin_payrolls, name='admin_list_payrolls'),
    path('admin-payrolls/create/', views.admin_payrolls, name='admin_create_payroll'),
    path('admin-payrolls/update/<int:payroll_id>/', views.admin_payrolls, name='admin_update_payroll'),
    path('admin-payrolls/delete/<int:payroll_id>/', views.admin_payrolls, name='admin_delete_payroll'),
    
    path('admin-sales/', views.admin_sales, name='admin_list_sales'),
    path('admin-sales/<int:sale_id>/details/', views.admin_sales, name='admin_sale_details'),
    path('admin-sales/delete/<sale_id>/', views.admin_sales, name='admin_delete_sale'),
    path('admin-sales/delete/item/<sale_id>/', views.admin_sales, name='admin_delete_sale_item'),
    path('admin-sales/delete/payment/<sale_id>/', views.admin_sales, name='admin_delete_sale_payment'),
    
    path('admin-payrolls/generate/', views.generate_payroll, name='generate_payroll'),
    path('admin-payrolls/report/', views.payroll_report, name='payroll_report'),

    path('shopping/', views.view_shopping, name='view_shopping'),
    path('shopping/add/<item_id>/', views.add_to_shopping, name='add_to_shopping'),
    path('shopping/adjust/<item_id>/', views.adjust_shopping_quantity, name='adjust_shopping_quantity'),
    path('shopping/adjust_shopping_discount/', views.adjust_shopping_discount, name='adjust_shopping_discount'),
    path('shopping/remove/<item_id>/', views.remove_shopping_item, name='remove_item'),
     
    # path('clients/', views.all_clients, name='clients'),
    # path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    # path('clients/add/', views.add_client, name='add_client'),
    # path('clients/edit/<int:client_id>/', views.edit_client, name='edit_client'),
    # path('clients/delete/<int:client_id>/', views.delete_client, name='delete_client'),
    # path('clients/details/<int:client_id>/', views.get_client_details, name='get_client_details'),
 
    path('sales/make_payment/', views.make_client_sale, name='make_payment'),
    path('sales/payment/success/<sale_id>/', views.sale_success, name='sale_success'),
    path('sale/print/<str:sale_id>/', views.print_sale, name='print_sale'),
    path('sales/make-rest-payment/<sale_id>/', views.sale_make_rest_payment, name='make_rest_payment'),

    path('delivery-slip/<sale_id>/', views.bordereau_livraison_view, name='delivery_slip'),
    path('update-sale-item/<item_id>/', views.update_sale_item_view, name='update_sale_item'),
    
    path('payrolls-dashboard/', views.payroll_dashboard, name='payroll_dashboard'),
    path('sales-dashboard/', views.sale_dashboard, name='sale_dashboard'),
    path('user-permissions/<user_id>/', views.user_permissions, name='user_permissions'),
    
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/create/', GroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/update/', GroupUpdateView.as_view(), name='group-update'),
    path('groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='group-delete'),
    
    
    
    
     
    # path('sale/wh/', webhook, name='webhook'),
    
    
    
   
    # # Lister toutes les factures
    # path('sales/', views.list_create_or_update_sale, name='sale_list'),
    # # Détails d'une facture spécifique
    # path('sale/<int:sale_id>/', views.sale_detail, name='sale_detail'),
    # # Créer une nouvelle facture
    # path('sale/create/', views.sale_create, name='sale_create'),
    # # Mettre à jour une facture existante
    # path('sale/<int:sale_id>/update/', views.sale_update, name='sale_update'),
    # # Supprimer une facture
    # path('sale/<int:sale_id>/delete/', views.sale_delete, name='sale_delete'),
    # # Imprimer la facture en PDF
    # path('sale/<int:sale_id>/print/', views.print_sale, name='print_sale'),

    
    
    
    # path('register/', RegisterView.as_view(), name='register'),
    # path('logout/', CustomLogoutView.as_view(), name='logout'),
    # path('employee/update/', EmployeeUpdateView.as_view(), name='employee_update'),
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('resend_activation_email/', ResendActivationEmailView.as_view(), name='resend_activation_email'),
    
    # Optional Additional Authentication Views
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    
    # # Optional Password Change URL
    # path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    # path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    
    # Optional Account Deletion View
    # Uncomment and implement this if you want to allow users to delete their accounts
    # path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),


]


