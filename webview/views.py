import os
from collections import defaultdict
from datetime import date, datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Q
from webview.utils import createAppSite, get_years_list, givenRate, notEmpty, parseDate, paymentStatusList, read_base64_file, safeDecimal, parseDatetime, save_pdf_file
from decimal import Decimal
from django.utils import timezone
from django.template.loader import render_to_string
from weasyprint import CSS, HTML
from django.contrib.contenttypes.models import ContentType

from .forms import CategoryForm, ClientForm, ExpiredStockForm, ProductForm, RegisterForm, LoginForm, EmployeeForm, StockForm
from .tokens import account_activation_token
from .context import shopping_contents
from .functions import send_email_with_attachment
from .models import AppSite, Category, Client, Country, ExpiredStock, Payroll, Product, Employee, Sale, SaleItem, Payment, Role, Stock
from .decorators import logout_required

PERMISSION_GROUP_TRANSLATIONS = {
    'country': 'Pays', 
    'role': 'Roles', 
    'employee': 'Utilisateurs/Employées', 
    'payroll': 'Payements salaire Employées', 
    'client': 'Clients', 
    'category': 'Categories de produits', 
    'product': 'Produits', 
    'stock': 'Stocks de produits', 
    'sale': 'Ventes de produits', 
    'saleitem': 'Item Article vendu', 
    'payment': 'Payement du Client',
    'expiredstock': 'Quantité Stock Périmé'
}


PERMISSION_TRANSLATIONS = {
    'Can add category': 'Peut ajouter une catégorie', #add_category
    'Can change category': 'Peut modifier une catégorie', #change_category
    'Can delete category': 'Peut supprimer une catégorie', #delete_category
    'Can view category': 'Peut voir une catégorie', #view_category
    
    'Can add client': 'Peut ajouter un client', #add_client
    'Can change client': 'Peut modifier un client', #change_client
    'Can delete client': 'Peut supprimer un client', #delete_client
    'Can view client': 'Peut voir un client', #view_client
    
    'Can add country': 'Peut ajouter un pays', #add_country
    'Can change country': 'Peut modifier un pays', #change_country
    'Can delete country': 'Peut supprimer un pays', #delete_country
    'Can view country': 'Peut voir un pays', #view_country
    
    'Can add employee': 'Peut ajouter un employé', #add_employee
    'Can change employee': 'Peut modifier un employé', #change_employee
    'Can delete employee': 'Peut supprimer un employé', #delete_employee
    'Can view employee': 'Peut voir un employé', #view_employee
    
    'Can add sale': 'Peut ajouter une vente', #add_sale
    'Can change sale': 'Peut modifier une vente', #change_sale
    'Can delete sale': 'Peut supprimer une vente', #delete_sale
    'Can view sale': 'Peut voir une vente', #view_sale
    
    'Can add sale item': 'Peut ajouter un article d\'une vente', #add_saleitem
    'Can change sale item': 'Peut modifier un article d\'une vente', #change_saleitem
    'Can delete sale item': 'Peut supprimer un article d\'une vente', #delete_saleitem
    'Can view sale item': 'Peut voir un article d\'une vente', #view_saleitem
    
    'Can add payment': 'Peut ajouter un paiement', #add_payment
    'Can change payment': 'Peut modifier un paiement', #change_payment
    'Can delete payment': 'Peut supprimer un paiement', #delete_payment
    'Can view payment': 'Peut voir un paiement', #view_payment
    
    'Can add payroll': 'Peut ajouter une paie', #add_payroll
    'Can change payroll': 'Peut modifier une paie', #change_payroll
    'Can delete payroll': 'Peut supprimer une paie', #delete_payroll
    'Can view payroll': 'Peut voir une paie', #view_payroll
    
    'Can add product': 'Peut ajouter un produit', #add_product
    'Can change product': 'Peut modifier un produit', #change_product
    'Can delete product': 'Peut supprimer un produit', #delete_product
    'Can view product': 'Peut voir un produit', #view_product
    
    'Can add role': 'Peut ajouter un rôle', #add_role
    'Can change role': 'Peut modifier un rôle', #change_role
    'Can delete role': 'Peut supprimer un rôle', #delete_role
    'Can view role': 'Peut voir un rôle', #view_role
    
    'Can add stock': 'Peut ajouter un stock', #add_stock
    'Can change stock': 'Peut modifier un stock', #change_stock
    'Can delete stock': 'Peut supprimer un stock', #delete_stock
    'Can view stock': 'Peut voir un stock', #view_stock
    
    'Can add expired stock': 'Peut ajouter un stock périmé', #add_expiredstock
    'Can change expired stock': 'Peut modifier un stock périmé', #change_expiredstock
    'Can delete expired stock': 'Peut supprimer un stock périmé', #delete_expiredstock
    'Can view expired stock': 'Peut voir un stock périmé', #view_expiredstock
}

unAutorizedMsg = 'Vous ne disposez pas de droit suffisant, contacter l\'administrateur'

def permissions_codenames(request):
    return list(request.user.user_permissions.values_list('codename', flat=True))
    
def has_permission(request, value=None):
    if value:
        return value in permissions_codenames or request.user.is_superuser
    return False

def has_perm(user, codename):
    # for permission in user.user_permissions.all():
    # print(permission.codename)
    return user.has_perm(f'webview.{codename}')

@login_required 
def home(request):
    # if request.user.is_superuser:
    #     #raise PermissionDenied
    #     messages.error(request, unAutorizedMsg)
    #     return redirect(reverse('home'))
    return redirect('products')
    # return render(request, 'home/index.html', {})

# class GroupListView(LoginRequiredMixin, ListView):
#     model = Group
#     template_name = 'groups/group_list.html'
#     context_object_name = 'groups'

# class GroupCreateView(LoginRequiredMixin, CreateView):
#     model = Group
#     form_class = GroupForm
#     template_name = 'groups/group_form.html'
#     success_url = reverse_lazy('group-list')
    
#     @login_required
#     def form_valid(self, form):
#         group = form.save(commit=False)
#         group.save()  # Save the group first
#         form.save_m2m()  # Save many-to-many relationships (permissions and users)
#         users = form.cleaned_data.get('users')
#         self.assign_group_to_users(group, users)
#         return super().form_valid(form)
    
#     @login_required
#     def assign_group_to_users(self, group, users):
#         """Assign the group to selected users."""
#         for user in users:
#             user.groups.add(group)

# class GroupUpdateView(LoginRequiredMixin, UpdateView):
#     model = Group
#     form_class = GroupForm
#     template_name = 'groups/group_form.html'
#     success_url = reverse_lazy('group-list')
    
#     @login_required
#     def get_object(self, queryset=None):
#         return get_object_or_404(Group, pk=self.kwargs.get('pk'))
    
#     @login_required
#     def form_valid(self, form):
#         group = form.save(commit=False)
#         group.save()  # Update the group
#         form.save_m2m()  # Save many-to-many relationships (permissions and users)
#         users = form.cleaned_data.get('users')
#         self.assign_group_to_users(group, users)
#         return super().form_valid(form)
    
#     @login_required
#     def assign_group_to_users(self, group, users):
#         """Reassign the group to the updated users."""
#         group.user_set.clear()  # Remove current users from the group
#         for user in users:
#             user.groups.add(group)

# class GroupDeleteView(LoginRequiredMixin, DeleteView):
#     model = Group
#     template_name = 'groups/group_confirm_delete.html'
#     success_url = reverse_lazy('group-list')

@login_required
def update_app_site(request):
    # Fetch the current site (assuming SITE_ID = 1)
    create_app_site = createAppSite(id=1)
    if create_app_site:
        messages.success(request, 'Site créé avec succès')
    else:
        messages.error(request, 'Désolé, une erreur s\'est produite! réessayer')
    return redirect(reverse('home'))
 
@login_required
def user_register(request):
    create_permission = 'add_category'
    update_permission = 'change_category'
    delete_permission = 'delete_category'
    view_permission = 'view_category'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    # if not request.user.is_superuser:
    #     messages.error(request, unAutorizedMsg)
    #     return redirect(reverse('home'))
    
    
    registered = False
    countries = Country.objects.filter(deleted=False)

    if request.method == 'POST':
    
        if not has_perm(request.user, create_permission):
            #raise PermissionDenied
            messages.error(request, unAutorizedMsg)
            return redirect(reverse('home'))
    
        if not has_perm(request.user, update_permission):
            #raise PermissionDenied
            messages.error(request, unAutorizedMsg)
            return redirect(reverse('home'))
        
        register_form = RegisterForm(request.POST)
        employee_form = EmployeeForm(request.POST, request.FILES)
        
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        employee_pic = request.FILES.get('employee_pic')

        if notEmpty(username) and notEmpty(email) and notEmpty(password) and notEmpty(password_confirm) and notEmpty(first_name) and notEmpty(last_name):
            if User.objects.filter(username=username).exists():
                register_form.add_error('username', _('Le nom d’utilisateur existe déjà. Veuillez en choisir un autre.'))
            elif User.objects.filter(email=email).exists():
                register_form.add_error('email', _('L’adresse email est déjà utilisée. Veuillez en fournir une autre.'))
            elif password != password_confirm:
                register_form.add_error('password_confirm', _('Les mots de passe ne concordent pas!'))
            else:
                if register_form.is_valid():
                    user = register_form.save(commit=False)
                    user.set_password(user.password)
                    # user.is_active = True
                    user.save()

                    try:
                        current_user = Employee.objects.get(user=request.user)
                    except Exception:
                        current_user = None
                    
                    employee = employee_form.save(commit=False)
                    employee.user = user
                    employee.created_by = current_user
                    
                    if employee_pic:
                        employee.employee_pic_thumb = employee_pic
                    
                    employee.save()
                    
                    registered = True
                    success_url = reverse_lazy('login')
                    
                    messages.success(request, _('Enrégistré avec succès'))
                    
                    return redirect(success_url)
                    # success = send_activation_email(request, user)
                    # if success:
                    #     messages.success(request, _('Veuillez confirmer votre adresse email pour compléter l’inscription.'))
                    #     success_url = reverse_lazy('login')
                    #     return redirect(success_url)
                    # else:
                    #     register_form.add_error(None, _('Une erreur est survenue lors de l’envoi de l’email de confirmation.'))
                else:
                    register_form.add_error(None, _('Vous devez bien renseigner tous les champs!'))
        else:
            register_form.add_error(None, _('Tous les champs sont obligatoires!'))
    else:
        register_form = RegisterForm()
        employee_form = EmployeeForm()

    return render(request, 'accounts/register.html', {
        'user_form': register_form,
        'employee_form': employee_form,
        'registered': registered,
        'countries': countries,
        'can_create': has_perm(request.user, create_permission),
        'can_update': has_perm(request.user, update_permission),
        'can_delete': has_perm(request.user, delete_permission),
    })

@logout_required
def user_login(request):
    view_permission = 'view_product'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        credential = request.POST.get('credential')
        password = request.POST.get('password')
        next_url = request.GET.get('next')
        
        if credential and password:
            try:
                user = User.objects.get(username=credential)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=credential)
                except User.DoesNotExist:
                    user = None
                    
                    
            if form.is_valid():
                if user is not None:
                    user = authenticate(request, username=user.username, password=password)
                    if user is not None:
                        if user.is_active:
                            
                            login(request, user)
                            try:
                                employee = Employee.objects.get(user=request.user)
                            except Employee.DoesNotExist:
                                employee = None

                            if not user.is_superuser and not employee:
                                # request.session['employee_picture_thumb'] = str(employee.employee_pic_thumb)
                                # request.session['employee_picture'] = str(employee.employee_pic)
                                return redirect('logout')

                            if not has_perm(user, view_permission):
                                messages.error(request, _('Vous n\'êtes pas autorisé à visualiser ce site. Contacter l\'administrateur!'))
                                return redirect('logout')
                                
                            messages.success(request, _('Connexion réussie!'))
                            if notEmpty(next_url):
                                return redirect(next_url)
                            else:
                                return HttpResponseRedirect(reverse('home'))
                        else:
                            # success = send_activation_email(request, user)
                            # if success:
                            #     messages.success(request, _('Veuillez confirmer votre adresse email pour compléter l’inscription.'))
                                # success_url = reverse_lazy('login')
                                # return redirect(success_url)
                            messages.error(request, _('Votre compte est désactivé. Contacter votre administrateur!'))
                    else:
                        messages.error(request, _('Nom d’utilisateur ou mot de passe incorrect.'))
                else:
                    messages.error(request, _('Nom d’utilisateur ou email incorrect.'))
            else:
                 messages.error(request, _('Nom d’utilisateur ou mot de passe incorrect.'))
        else:
            messages.error(request, _('Veuillez entrer le nom d’utilisateur ou l’email et le mot de passe.'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html',{ 'form': form })

@logout_required
def activate_email(request, uidb64, token):
    """
    Activates the user account.
    """
    try:
        # Decode the UID and retrieve the User instance
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)  # Retrieve the User object
        employee = Employee.objects.get(user=user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, Employee.DoesNotExist):
        user = None
        employee = None
    

    if user and employee and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        # user.is_superuser = True
        user.save()
        
        employee.email_verified = True
        employee.save()
        messages.success(request, _('Your account has been activated successfully.'))
        return redirect('login')
    else:
        messages.error(request, _('The activation link is invalid or has expired.'))
    return redirect('register')

@login_required
def user_logout(request):
    logout(request)
    # messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect(reverse('login'))

@login_required
def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # create_permission = 'add_product'
    # update_permission = 'change_product'
    # delete_permission = 'delete_product'
    view_permission = 'view_product'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        # return redirect(reverse('home'))
        return redirect('logout')
    
    categories = Category.objects.filter(deleted=False)
    products = Product.objects.filter(deleted=False, is_available=True)
    search = None
    category = None
    
    if request.method == 'GET':
        search = request.GET.get('search', None)
        category = request.GET.get('category', None)
        if search and products:
            products = products.filter((Q(name__icontains=search) | Q(description__icontains=search)))
        
        if category and products:
            products = products.filter(category__id=category)
    
    return render(request, 'home/products.html', { 'products': products, 'search': search if search or search is not None else '', 'categories': categories, 'selected_category_id':category })

@login_required
def product_detail(request, product_id):
    """ A view to show individual product details """
    # create_permission = 'add_product'
    # update_permission = 'change_product'
    # delete_permission = 'delete_product'
    view_permission = 'view_product'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    try:
        product = Product.objects.get(pk=product_id)
    except Exception:
        product = None
        
    if product:
        return render(request, 'products/product_detail.html', {'product': product})
    else:
        return redirect('products')

@login_required
def get_product_details(request, product_id):
    """ Get product details for editing """
    # create_permission = 'add_product'
    # update_permission = 'change_product'
    # delete_permission = 'delete_product'
    view_permission = 'view_product'
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        product = None
    
    data = {
        'category': product.category if product else '',
        'name': product.name if product else '',
        'description': product.description if product else '',
        'price': product.price if product else '',
        'is_available': product.is_available if product else '',
        'imageUrl': product.imageUrl if product else '',
        'shoppingQuantiy': str(request.session['shopping'][f'{product_id}']) if product else 0
    }
    return JsonResponse({'form': data})

@login_required
def admin_products(request, product_id=None):
    """ Add a product to the store """
    create_permission = 'add_product'
    update_permission = 'change_product'
    delete_permission = 'delete_product'
    view_permission = 'view_product'
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        productAction = request.POST.get('product_action') 
        try:
            current_user = Employee.objects.get(user=request.user)
        except Exception:
            current_user = None
            
        if productAction == 'create':
            if not has_perm(request.user, create_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.user = current_user
                product.save()
                messages.success(request, f'Successfully added product: {product.name}')
                return redirect(reverse('admin_list_products'))
            else:
                messages.error(request, 'Failed to add product. Please ensure the form is valid.')
        elif productAction == 'update':
            if not has_perm(request.user, update_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if isinstance(product_id, int):
                try:
                    product = Product.objects.get(pk=product_id)
                except Exception:
                    product = None
                
                if product:
                    try:
                        form = ProductForm(request.POST, request.FILES, instance=product)
                        if form.is_valid():
                            product = form.save(commit=False)
                            product.updated_by = current_user
                            product.updated_at = timezone.now()
                            product.save()
                            messages.success(request, f'Successfully updated product: {product.name}')
                            # return redirect(reverse('product_detail', args=[product.id]))
                            return redirect(reverse('admin_list_products'))
                        else:
                            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
                    except Product.DoesNotExist:
                        messages.error(request, 'Error while saving data.')
                else:
                    messages.error(request, 'Product not found.')
                    return redirect(reverse('admin_list_products'))
        elif productAction == 'delete':
            if not has_perm(request.user, delete_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if isinstance(product_id, int):
                try:
                    product = Product.objects.get(id=product_id)
                    product.deleted = True
                    product.deleted_by = current_user
                    product.deleted_at = timezone.now()
                    product.save()
                    # product.delete()
                    messages.success(request, 'Product deleted successfully!')
                    return redirect(reverse('admin_list_products'))
                except Product.DoesNotExist:
                    messages.error(request, 'Product not found.')
        else:
            messages.error(request, "Pas d'action trouvé!")
            return redirect(reverse('admin_list_products'))
    else:
        form = ProductForm()
    
    stock_form = StockForm() 
    products = Product.objects.filter(deleted=False)
    
    return render(
        request, 
        'admins/products.html', { 
         'form': form, 
         'stock_form': stock_form, 
         'products': products,
         'can_create': has_perm(request.user, create_permission),
         'can_update': has_perm(request.user, update_permission),
         'can_delete': has_perm(request.user, delete_permission),
        })

@login_required
def admin_clients_details(request, client_id):
    """ Get client details for editing """
    # # create_permission = 'add_client'
    # # update_permission = 'change_client'
    # # delete_permission = 'delete_client'
    # view_permission = 'view_client'
    
    # if not has_perm(request.user, view_permission):
    #     #raise PermissionDenied
    #     messages.error(request, unAutorizedMsg)
    #     return redirect(reverse('home'))
    
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        client = None
    data = {
        'first_name': client.first_name if client else '',
        'last_name': client.last_name if client else '',
        'email': client.email if client else '',
        'phone_number': client.phone_number if client else '',
        'phone_number_other': client.phone_number_other if client else '',
        'address': client.address if client else '',
        'country': client.country if client else '',
        'city': client.city if client else '',
        'company': client.company if client else '',
    }
    return JsonResponse({'form': data})

@login_required
def admin_clients(request, client_id=None):
    """ Add a client to the store """
    create_permission = 'add_client'
    update_permission = 'change_client'
    delete_permission = 'delete_client'
    view_permission = 'view_client'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))

    if request.method == 'POST':
        clientAction = request.POST.get('client_action')
        try:
            current_user = Employee.objects.get(user=request.user)
        except Exception:
            current_user = None
        if clientAction == 'create':
            if not has_perm(request.user, create_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            form = ClientForm(request.POST, request.FILES)
            if form.is_valid():
                client = form.save(commit=False)
                client.user = current_user
                client.save()
                messages.success(request, f'Successfully added client: {client.full_name}')
                return redirect(reverse('admin_list_clients'))
            else:
                messages.error(request, 'Failed to add client. Please ensure the form is valid.')
        elif clientAction == 'update':
            if not has_perm(request.user, update_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if isinstance(client_id, int):
                try:
                    client = Client.objects.get(pk=client_id)
                except Exception:
                    client = None
                
                if client:
                    try:
                        form = ClientForm(request.POST, request.FILES, instance=client)
                        if form.is_valid():
                            client = form.save(commit=False)
                            client.updated_by = current_user
                            client.updated_at = timezone.now()
                            client.save()
                            messages.success(request, f'Successfully updated client: {client.full_name}')
                            # return redirect(reverse('client_detail', args=[client.id]))
                            return redirect(reverse('admin_list_clients'))
                        else:
                            messages.error(request, 'Failed to update client. Please ensure the form is valid.')
                    except Client.DoesNotExist:
                        messages.error(request, 'Error while saving data.')
                else:
                    messages.error(request, 'Client not found.')
                    return redirect(reverse('admin_list_clients'))
        elif clientAction == 'delete':
            if not has_perm(request.user, delete_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if isinstance(client_id, int):
                try:
                    client = Client.objects.get(id=client_id)
                    client.deleted = True
                    client.deleted_by = current_user
                    client.deleted_at = timezone.now()
                    client.save()
                    # client.delete()
                    messages.success(request, 'Client deleted successfully!')
                    return redirect(reverse('admin_list_clients'))
                except Client.DoesNotExist:
                    messages.error(request, 'Client not found.')
        else:
            messages.error(request, "Pas d'action trouvé!")
            return redirect(reverse('admin_list_clients'))
    else:
        form = ClientForm()
        
        
    clients = Client.objects.filter(deleted=False)
    return render(request, 'admins/clients.html', { 'form': form, 'clients': clients })

@login_required
def admin_users(request, user_id=None):
    """ Add, update, delete or filter users in the store """
    create_permission = 'add_employee'
    update_permission = 'change_employee'
    delete_permission = 'delete_employee'
    view_permission = 'view_employee'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    employees = None
    filter_roles = []

    if request.method == 'POST':
        rpg = request.POST.get
        userAction = rpg('user_action')
        try:
            current_user = Employee.objects.get(user=request.user)
        except Exception:
            current_user = None
                
        if userAction == 'create':
            if not has_perm(request.user, create_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            register_form = RegisterForm(request.POST)
            employee_form = EmployeeForm(request.POST, request.FILES)
            
            if register_form.is_valid() and employee_form.is_valid():
                password = rpg('password')
                password_confirm = rpg('password_confirm')
                employee_pic = request.FILES.get('employee_pic')
                
                if password != password_confirm:
                    register_form.add_error('password_confirm', _('Les mots de passe ne concordent pas!'))
                else:
                    user = register_form.save(commit=False)
                    user.set_password(password)  # Utiliser 'password' directement
                    # user.is_active = True
                    user.save()

                    employee = employee_form.save(commit=False)
                    employee.user = user
                    employee.created_by = current_user

                    if employee_pic:
                        employee.employee_pic = employee_pic
                        employee.employee_pic_thumb = employee_pic

                    employee.save()
                    
                    # Now handle Many-to-Many field (roles)
                    roles = request.POST.getlist('roles')  # Get the list of roles from the form
                    if roles:
                        employee.roles.set(roles)  # Add roles after saving employee
                        
                    messages.success(request, _('Enrégistré avec succès'))
                    
                    return redirect(reverse('admin_list_users'))
                
                    # if send_activation_email(request, user):
                    #     messages.success(request, _('L\'utilisateur doit confirmer son adresse email pour compléter l’inscription.'))
                    #     return redirect(reverse('admin_list_users'))
                    # else:
                    #     messages.error(request, 'Erreur lors de l’envoi de l\'email de confirmation.')
            else:
                messages.error(request, 'Veuillez remplir correctement tous les champs.')
        elif userAction == 'update' and user_id:
            if not has_perm(request.user, update_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            try:
                user = User.objects.get(pk=user_id)
                employee = Employee.objects.get(user=user)

                register_form = RegisterForm(request.POST, instance=user)
                employee_form = EmployeeForm(request.POST, request.FILES, instance=employee)

                username = request.POST.get('username')
                email = request.POST.get('email')
                is_active = request.POST.get('is_active')

                user.username = username
                user.email = email
                user.is_active = is_active == 'on' or is_active == '1' or is_active == 1 or is_active == 'yes' or is_active == 'true' or is_active

                password = request.POST.get('password')
                password_confirm = request.POST.get('password_confirm')

                if password and password == password_confirm:
                    user.set_password(password)

                user.save()
                
                employee = employee_form.save(commit=False)
                employee.updated_by = current_user
                employee.updated_at = timezone.now()

                if request.FILES.get('employee_pic'):
                    employee.employee_pic = request.FILES.get('employee_pic')
                    employee.employee_pic_thumb = employee.employee_pic

                employee.save()

                roles = request.POST.getlist('roles')
                if roles:
                    employee.roles.set(roles) 

                messages.success(request, f'Utilisateur {employee.user.username} mis à jour avec succès.')
                return redirect(reverse('admin_list_users'))
            except (User.DoesNotExist, Employee.DoesNotExist):
                messages.error(request, 'Utilisateur introuvable.')
        elif userAction == 'delete':
            if not has_perm(request.user, delete_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if user_id:
                try:
                    employee = Employee.objects.get(id=user_id)
                    user = employee.user
                    employee.deleted = True
                    employee.deleted_by = current_user
                    employee.deleted_at = timezone.now()
                    employee.save()
                    
                    # user.deleted = True
                    user.is_active = False
                    user.is_superuser = False
                    user.is_staff = False
                    user.is_authenticated = False
                    user.user_permissions.clear()
                    user.save()
                    
                    # employee.delete()
                    # user.delete()
                    messages.success(request, 'Utilisateur supprimé avec succès!')
                    return redirect(reverse('admin_list_users'))
                except Employee.DoesNotExist:
                    messages.error(request, 'Utilisateur introuvable.')
        elif userAction == 'make_employee_payment':
            if not has_perm(request.user, create_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if user_id:
                employee_salary_date = parseDatetime(rpg('employee_salary_date')) if rpg('employee_salary_date') else None
                employee_salary_brut = safeDecimal(rpg('employee_salary_brut'), tryNull=True)
                employee_cnss = safeDecimal(rpg('employee_cnss'), tryNull=True)
                employee_irpp = safeDecimal(rpg('employee_irpp'), tryNull=True)
                employee_other_deductions = safeDecimal(rpg('employee_other_deductions'), tryNull=True)
                employee_commission = safeDecimal(rpg('employee_commission'))

                if employee_salary_date and employee_salary_brut:
                    employee_user = Employee.objects.get(id=user_id)
                    payroll = Payroll(
                        employee=employee_user,
                        date=employee_salary_date,
                        salary_brut=employee_salary_brut,
                        cnss=employee_cnss,
                        irpp=employee_irpp,
                        other_deductions=employee_other_deductions,
                        commission=employee_commission,
                        created_by=current_user,
                        created_at = timezone.now()
                    )
                    payroll.save()

                    messages.success(request, "Paiement effectué avec succès!")
                    return redirect(reverse('admin_list_users'))
                else:
                    register_form = RegisterForm()
                    employee_form = EmployeeForm()
                    messages.error(request, "Erreur lors du paiement, veuillez réessayer.")
        elif userAction == 'roles_filter':
            eRoles = request.POST.getlist('employee_roles')
            eRoles = [item for item in eRoles if item != '']
            if notEmpty(eRoles):
                filter_roles = eRoles
                employees = Employee.objects.filter(user__is_superuser=False, role__id__in=filter_roles,  deleted=False)

    else:
        register_form = RegisterForm()
        employee_form = EmployeeForm()

    employees = Employee.objects.filter(user__is_superuser=False, deleted=False) if not employees and employees is None else employees
    countries = Country.objects.filter(deleted=False)
    roles = Role.objects.filter(deleted=False)
    
    # permissions = Permission.objects.all()
    
    models = [Country, Role, Employee, Payroll, Client, Category, Product, Stock, ExpiredStock, Sale, SaleItem, Payment]
    content_types = [ContentType.objects.get_for_model(model) for model in models]
    permissions = Permission.objects.filter(content_type__in=content_types)
    
    grouped_permissions = defaultdict(list)
    
    for permission in permissions:
        model_name = PERMISSION_GROUP_TRANSLATIONS.get(permission.content_type.model, permission.content_type.model)   # Get the model name related to the permission
        translated_permission_name = PERMISSION_TRANSLATIONS.get(permission.name, permission.name)  # Fallback to original if not found
        grouped_permissions[model_name].append({
            'id': permission.id,
            'name': translated_permission_name,
            'codename': permission.codename
        })
        # print(translated_permission_name)
    grouped_permissions = dict(grouped_permissions)

    return render(request, 'admins/employees.html', {
        'employees': employees,
        'roles': roles,
        'filter_roles': filter_roles,
        'user_form': register_form,
        'employee_form': employee_form,
        'countries': countries,
        'grouped_permissions': grouped_permissions,
        'can_create': has_perm(request.user, create_permission),
        'can_update': has_perm(request.user, update_permission),
        'can_delete': has_perm(request.user, delete_permission),
    })
    
@login_required
def user_permissions(request, user_id):
    create_permission = 'add_employee'
    update_permission = 'change_employee'
    delete_permission = 'delete_employee'
    view_permission = 'view_employee'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    if not has_perm(request.user, create_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    if not has_perm(request.user, update_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    if not has_perm(request.user, delete_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        permission_ids = request.POST.getlist('permissions')
        
        user = User.objects.get(id=user_id)
        # Clear existing permissions
        user.user_permissions.clear()
        
        # Add selected permissions
        for perm_id in permission_ids:
            perm = Permission.objects.get(id=perm_id)
            user.user_permissions.add(perm)

    return redirect('admin_list_users')

@login_required
def admin_categories(request, category_id=None):
    """ Add a category to the store """
    create_permission = 'add_category'
    update_permission = 'change_category'
    delete_permission = 'delete_category'
    view_permission = 'view_category'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))

    if request.method == 'POST':
        categoryAction = request.POST.get('category_action')
        try:
            current_user = Employee.objects.get(user=request.user)
        except Exception:
            current_user = None
            
        if categoryAction == 'create':
            if not has_perm(request.user, create_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = current_user
                category.created_at = timezone.now()
                category.save()
                
                messages.success(request, f'Successfully added category {category.name}')
              
                redirect_url = request.POST.get('redirect_url')
                if (notEmpty(redirect_url)):
                    return redirect(redirect_url)
                else:
                    return redirect(reverse('admin_list_categories'))
            else:
                messages.error(request, 'Failed to add category. Please ensure the form is valid.')
        elif categoryAction == 'update':
            if not has_perm(request.user, update_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if isinstance(category_id, int):
                try:
                    category = Category.objects.get(pk=category_id)
                except Exception:
                    category = None
                
                if category:
                    try:
                        form = CategoryForm(request.POST, request.FILES, instance=category)
                        if form.is_valid():
                            category = form.save(commit=False)
                            category.updated_by = current_user
                            category.updated_at = timezone.now()
                            category.save()
                            messages.success(request, f'Successfully updated category {category.name}')
                            # return redirect(reverse('category_detail', args=[category.id]))
                            return redirect(reverse('admin_list_categories'))
                        else:
                            messages.error(request, 'Failed to update category. Please ensure the form is valid.')
                    except Category.DoesNotExist:
                        messages.error(request, 'Error while saving data.')
                else:
                    messages.error(request, 'category not found.')
                    return redirect(reverse('admin_list_categories'))
        elif categoryAction == 'delete':
            if not has_perm(request.user, delete_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if isinstance(category_id, int):
                try:
                    category = Category.objects.get(id=category_id)
                    category.deleted = True
                    category.updated_by = current_user
                    category.deleted_at = timezone.now()
                    category.save()
                    # category.delete()
                    messages.success(request, 'category deleted successfully!')
                    return redirect(reverse('admin_list_categories'))
                except Category.DoesNotExist:
                    messages.error(request, 'category not found.')
        else:
            messages.error(request, "Pas d'action trouvé!")
            return redirect(reverse('admin_list_categories'))
    else:
        form = CategoryForm()
        
    categories = Category.objects.filter(deleted=False)
    return render(request, 'admins/categories.html', { 'form': form, 'categories': categories })

@login_required
def admin_stocks(request, stock_id=None):
    """ Add a stock to the store """
    create_permission = 'add_stock'
    update_permission = 'change_stock'
    delete_permission = 'delete_stock'
    view_permission = 'view_stock'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))

    if request.method == 'POST':
        stockAction = request.POST.get('stock_action')
        try:
            current_user = Employee.objects.get(user=request.user)
        except Exception:
            current_user = None
            
        if stockAction == 'create':
            if not has_perm(request.user, create_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            form = StockForm(request.POST, request.FILES)
            if form.is_valid():
                stock = form.save(commit=False)
                stock.user = current_user
                stock.save()
                
                messages.success(request, f'Successfully added stock {stock.quantity} to {stock.product.name}')
              
                redirect_url = request.POST.get('redirect_url')
                if (notEmpty(redirect_url)):
                    return redirect(redirect_url)
                else:
                    return redirect(reverse('admin_list_stocks'))
            else:
                messages.error(request, 'Failed to add stock. Please ensure the form is valid.')
        elif stockAction == 'update':
            if not has_perm(request.user, update_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if isinstance(stock_id, int):
                try:
                    stock = Stock.objects.get(pk=stock_id)
                except Exception:
                    stock = None
                
                if stock:
                    try:
                        form = StockForm(request.POST, request.FILES, instance=stock)
                        if form.is_valid():
                            stock = form.save(commit=False)
                            stock.updated_by = current_user
                            stock.updated_at = timezone.now()
                            stock.save()
                            messages.success(request, f'Successfully updated stock {stock.quantity} to {stock.product.name}')
                            # return redirect(reverse('stock_detail', args=[stock.id]))
                            return redirect(reverse('admin_list_stocks'))
                        else:
                            messages.error(request, 'Failed to update stock. Please ensure the form is valid.')
                    except Stock.DoesNotExist:
                        messages.error(request, 'Error while saving data.')
                else:
                    messages.error(request, 'stock not found.')
                    return redirect(reverse('admin_list_stocks'))
        elif stockAction == 'delete':
            if not has_perm(request.user, delete_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if isinstance(stock_id, int):
                try:
                    stock = Stock.objects.get(id=stock_id)
                    stock.deleted = True
                    stock.deleted_by = current_user
                    stock.deleted_at = timezone.now()
                    stock.save()
                    # stock.delete()
                    messages.success(request, 'stock deleted successfully!')
                    return redirect(reverse('admin_list_stocks'))
                except Stock.DoesNotExist:
                    messages.error(request, 'stock not found.')
        else:
            messages.error(request, "Pas d'action trouvé!")
            return redirect(reverse('admin_list_stocks'))
    else:
        form = StockForm()
        
        
    stocks = Stock.objects.filter(deleted=False)
    return render(request, 'admins/stocks.html', { 'form': form, 'stocks': stocks })

@login_required
def admin_expired_stocks(request, expired_stock_id=None):
    """ Add a expired stock to the store """
    create_permission = 'add_expiredstock'
    update_permission = 'change_expiredstock'
    delete_permission = 'delete_expiredstock'
    view_permission = 'view_expiredstock'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))

    if request.method == 'POST':
        expiredStockAction = request.POST.get('expired_stock_action')
        try:
            current_user = Employee.objects.get(user=request.user)
        except Exception:
            current_user = None
            
        if expiredStockAction == 'create':
            if not has_perm(request.user, create_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            form = ExpiredStockForm(request.POST, request.FILES)
            if form.is_valid():
                expired_stock = form.save(commit=False)
                expired_stock.user = current_user
                expired_stock.save()
                
                messages.success(request, f'Vous avez déclarer {expired_stock.quantity} produits périmé pour {expired_stock.product.name}')
              
                redirect_url = request.POST.get('redirect_url')
                if (notEmpty(redirect_url)):
                    return redirect(redirect_url)
                else:
                    return redirect(reverse('admin_list_expired_stocks'))
            else:
                messages.error(request, 'Failed to add expired stock. Please ensure the form is valid.')
        elif expiredStockAction == 'update':
            if not has_perm(request.user, update_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if isinstance(expired_stock_id, int):
                try:
                    expired_stock = ExpiredStock.objects.get(pk=expired_stock_id)
                except Exception:
                    expired_stock = None
                
                if expired_stock:
                    try:
                        form = ExpiredStockForm(request.POST, request.FILES, instance=expired_stock)
                        if form.is_valid():
                            expired_stock = form.save(commit=False)
                            expired_stock.updated_by = current_user
                            expired_stock.updated_at = timezone.now()
                            expired_stock.save()
                            messages.success(request, f'Vous avez modifier la déclaration de péromption de {expired_stock.quantity} pour {expired_stock.product.name}')
                            # return redirect(reverse('expired_stock_detail', args=[expired_stock.id]))
                            return redirect(reverse('admin_list_expired_stocks'))
                        else:
                            messages.error(request, 'Failed to update expired stocks. Please ensure the form is valid.')
                    except ExpiredStock.DoesNotExist:
                        messages.error(request, 'Error while saving data.')
                else:
                    messages.error(request, 'expired stock not found.')
                    return redirect(reverse('admin_list_expired_stocks'))
        elif expiredStockAction == 'delete':
            if not has_perm(request.user, delete_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if isinstance(expired_stock_id, int):
                try:
                    expired_stock = ExpiredStock.objects.get(id=expired_stock_id)
                    expired_stock.deleted = True
                    expired_stock.deleted_by = current_user
                    expired_stock.deleted_at = timezone.now()
                    expired_stock.save()
                    # expired_stock.delete()
                    messages.success(request, 'expired stocks deleted successfully!')
                    return redirect(reverse('admin_list_expired_stocks'))
                except ExpiredStock.DoesNotExist:
                    messages.error(request, 'expired stocks not found.')
        else:
            messages.error(request, "Pas d'action trouvé!")
            return redirect(reverse('admin_list_expired_stocks'))
    else:
        form = ExpiredStockForm()
        
        
    expired_stocks = ExpiredStock.objects.filter(deleted=False)
    return render(request, 'admins/expired_stocks.html', { 'form': form, 'expired_stocks': expired_stocks })


@login_required
def admin_sales(request, sale_id=None):
    """ Add a sale to the store """
    # create_permission = 'add_sale'
    # update_permission = 'change_sale'
    delete_permission = 'delete_sale'
    view_permission = 'view_sale'

    # create_item_permission = 'add_saleitem'
    # update_item_permission = 'change_saleitem'
    delete_item_permission = 'delete_saleitem'
    # view_item_permission = 'view_saleitem'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    sales = None
    filter_status = []
    filter_clients = []
    
    fDate = datetime.now()
    fsdate = fDate.replace(hour=0, minute=0, second=0, microsecond=1000)  # 00:00:00
    fedate = fDate.replace(hour=23, minute=59, second=59, microsecond=999999)  # 23:59:59
    
    if 'filter_start_date' in request.session and 'filter_end_date' in request.session:
        ffsdate = parseDate(request.session['filter_start_date']) if notEmpty(request.session['filter_start_date']) else fsdate
        ffedate = parseDate(request.session['filter_end_date']) if notEmpty(request.session['filter_end_date']) else fedate
        
        filter_start_date = ffsdate.replace(hour=0, minute=0, second=0, microsecond=1000)
        filter_end_date = ffedate.replace(hour=23, minute=59, second=59, microsecond=999999)
    else:
        filter_start_date = fsdate
        filter_end_date = fedate

    
    if request.method == 'POST':
        saleAction = request.POST.get('sale_action')
        try:
            current_user = Employee.objects.get(user=request.user)
        except Exception:
            current_user = None

        if saleAction == 'delete':
            if not has_perm(request.user, delete_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if sale_id:
                try:
                    sale = Sale.objects.get(id=sale_id)
                    sale.deleted = True
                    sale.deleted_by = current_user
                    sale.deleted_at = timezone.now()
                    sale.save()
                    
                    # sale.delete()
                    messages.success(request, 'Sale deleted successfully!')
                    return redirect(reverse('admin_list_sales'))
                except Sale.DoesNotExist:
                    messages.error(request, 'Sale not found.')
        elif saleAction == 'delete-sale-item':
            if not has_perm(request.user, delete_item_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if sale_id:
                try:
                    saleItem = SaleItem.objects.get(id=sale_id)
                    saleItem.deleted = True
                    saleItem.deleted_by = current_user
                    saleItem.deleted_at = timezone.now()
                    saleItem.save()
                    
                    # sale.delete()
                    messages.success(request, 'Sale Item deleted successfully!')
                    return redirect(reverse('admin_list_sales'))
                except Sale.DoesNotExist:
                    messages.error(request, 'Sale Item not found.')
        elif saleAction == 'delete-sale-payment':
            if not has_perm(request.user, delete_permission) or not has_perm(request.user, delete_item_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if sale_id:
                try:
                    salePayment = Payment.objects.get(id=sale_id)
                    salePayment.deleted = True
                    salePayment.deleted_by = current_user
                    salePayment.deleted_at = timezone.now()
                    salePayment.save()
                    
                    # sale.delete()
                    messages.success(request, 'Sale Payment deleted successfully!')
                    return redirect(reverse('admin_list_sales'))
                except Sale.DoesNotExist:
                    messages.error(request, 'Sale Payment not found.')
        elif saleAction == 'sales_filter':
            eStatus = request.POST.getlist('sale_status')
            eStatus = [item for item in eStatus if item != '']
            
            eClients = request.POST.getlist('sale_clients')
            eClients = [item for item in eClients if item != '']
            
            eStartDate = request.POST.get('sale_start_date')
            eEndDate = request.POST.get('sale_end_date')
            
            sales = Sale.objects.filter(deleted=False)
            
            if notEmpty(eStatus) :
                filter_status = eStatus
                sales = [sale for sale in sales if sale.status['id'] in filter_status]
                
            if notEmpty(eClients) :
                filter_clients = eClients
                sales = [sale for sale in sales if str(sale.client.id) in filter_clients]
                
            if notEmpty(eStartDate) and notEmpty(eEndDate) :
                filter_start_date = datetime.strptime(eStartDate, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=1000)
                filter_end_date = datetime.strptime(eEndDate, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=999999)
                
        
    sales = Sale.objects.filter(deleted=False) if not sales and sales is None else sales
    # sales = [sale for sale in sales if filter_start_date <= sale.date <= filter_end_date]
    sales = [sale for sale in sales if filter_start_date <= sale.date.replace(tzinfo=None) <= filter_end_date]
    
    clients = Client.objects.filter(deleted=False)
    
  
    total_discount = sum(sale.discount for sale in sales) if sales and len(sales) > 0 else 0.0
    total_tax_amount = sum(sale.tax_amount for sale in sales) if sales and len(sales) > 0 else 0.0
    total_ht_amount = sum(sale.ht_amount for sale in sales) if sales and len(sales) > 0 else 0.0
    total_ttc_amount = sum(sale.ttc_amount for sale in sales) if sales and len(sales) > 0 else 0.0
    total_payments_amount = sum(sale.payments_amount for sale in sales) if sales and len(sales) > 0 else 0.0
    
    request.session['filter_status'] = filter_status
    request.session['filter_clients'] = filter_clients
    request.session['filter_start_date'] = filter_start_date.strftime('%Y-%m-%d')
    request.session['filter_end_date'] = filter_end_date.strftime('%Y-%m-%d')

    return render(
        request, 
        'admins/sales.html', {
            'sales': sales, 
            'filter_status': request.session['filter_status'],
            'filter_clients': request.session['filter_clients'],
            'filter_start_date': request.session['filter_start_date'],
            'filter_end_date': request.session['filter_end_date'],
            'status': paymentStatusList() ,
            'clients': clients,

            'total_discount': total_discount, 
            'total_tax_amount': total_tax_amount, 
            'total_ht_amount': total_ht_amount, 
            'total_ttc_amount': total_ttc_amount, 
            'total_payments_amount': total_payments_amount, 
            
            'hasSales': len(sales) > 0
        })

@login_required
def admin_payrolls(request, payroll_id=None):
    """ Add a payroll to the store """
    create_permission = 'add_payroll'
    update_permission = 'change_payroll'
    delete_permission = 'delete_payroll'
    view_permission = 'view_payroll'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))

    if request.method == 'POST':
        rpg = request.POST.get
        payrollAction = rpg('payroll_action')
        try:
            employee = Employee.objects.get(id=rpg('employee'))
            current_user = Employee.objects.get(user=request.user)
        except Exception:
            employee = None
            current_user = None
        
        if payrollAction == 'create' or payrollAction == 'update' and employee and employee is not None:
            
            salary_date = parseDate(rpg('salary_date')) if rpg('salary_date') else None
            salary_brut = safeDecimal(rpg('salary_brut'), tryNull=True)
            salary_cnss = safeDecimal(rpg('salary_cnss'), tryNull=True)
            salary_irpp = safeDecimal(rpg('salary_irpp'), tryNull=True)
            salary_other_deductions = safeDecimal(rpg('salary_other_deductions'), tryNull=True)
            salary_commission = safeDecimal(rpg('salary_commission'))
            
            if salary_brut:
                if payrollAction == 'create':
                    if not has_perm(request.user, create_permission):
                        #raise PermissionDenied
                        messages.error(request, unAutorizedMsg)
                        return redirect(reverse('home'))
                
                    try:
                        payroll = Payroll(
                            employee=employee,
                            date=salary_date,
                            salary_brut=salary_brut,
                            cnss=salary_cnss,
                            irpp=salary_irpp,
                            other_deductions=salary_other_deductions,
                            commission=salary_commission,
                            created_by=current_user
                        )
                        payroll.save()
                        
                        messages.success(request, 'Paiement effectué avec succès!')
                        return redirect(reverse('admin_list_payrolls'))
                    except payroll.DoesNotExist:
                        messages.error(request, 'Erreur lors du paiement, veuillez réessayer.')
                elif payrollAction == 'update':
                    if not has_perm(request.user, update_permission):
                        #raise PermissionDenied
                        messages.error(request, unAutorizedMsg)
                        return redirect(reverse('home'))
                    
                    if payroll_id:
                        try:
                            payroll = Payroll.objects.get(pk=payroll_id)
                        except Exception:
                            payroll = None
                        
                        if payroll:
                            try:
                                payroll.date = salary_date
                                payroll.salary_brut = salary_brut
                                payroll.cnss = salary_cnss
                                payroll.irpp = salary_irpp
                                payroll.other_deductions = salary_other_deductions
                                payroll.commission = salary_commission
                                payroll.updated_by = current_user
                                payroll.updated_at = timezone.now()
                                payroll.save()
                                
                                messages.success(request, 'paiement modifié avec succès')
                                return redirect(reverse('admin_list_payrolls'))
                            except payroll.DoesNotExist:
                                messages.error(request, 'Erreur lors du paiement, veuillez réessayer.')
                        else:
                            messages.error(request, 'Erreur lors du paiement, veuillez réessayer.')
                            return redirect(reverse('admin_list_payrolls'))
            else:
                messages.error(request, "Renseignez le salaire de sase")
                return redirect(reverse('admin_list_payrolls'))
        elif payrollAction == 'delete':
            if not has_perm(request.user, delete_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            if payroll_id:
                try:
                    payroll = Payroll.objects.get(id=payroll_id)
                    payroll.deleted = True
                    payroll.deleted_by = current_user
                    payroll.deleted_at = timezone.now()
                    
                    payroll.save()
                    # payroll.delete()
                    messages.success(request, 'paiement supprimé avec succès!')
                    return redirect(reverse('admin_list_payrolls'))
                except Payroll.DoesNotExist:
                    messages.error(request, 'Erreur lors de la suppression du paiement, veuillez réessayer.')
        else:
            messages.error(request, "Pas d'action trouvé!")
            return redirect(reverse('admin_list_payrolls'))
        
    payrolls = Payroll.objects.filter(deleted=False)
    employees = Employee.objects.filter(user__is_superuser=False, deleted=False)
    
    return render(
        request, 
        'admins/payrolls.html', { 
            'payrolls': payrolls, 
            'employees': employees,
            'can_create': has_perm(request.user, create_permission),
            'can_update': has_perm(request.user, update_permission),
            'can_delete': has_perm(request.user, delete_permission),
        })

@login_required
def view_shopping(request):
    """ A view that renders the bag contents page """
    if not request.session.get('shopping', {}):
        # messages.error(request, "Pas d'article en cours de vente pour le moment")
        return redirect(reverse('products'))
    
    clients = Client.objects.filter(deleted=False)
    countries = Country.objects.filter(deleted=False)
    return render(request, 'shopping/shopping.html', {'clients': clients, 'countries': countries})

@login_required
def add_to_shopping(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    try:
        quantity = int(request.POST.get('quantity', 0))
        redirect_url = request.POST.get('redirect_url')
        if quantity > 0:
            try:
                product = Product.objects.get(pk=item_id)
            except Exception:
                product = None
            
            if product:
                shopping = request.session.get('shopping', {})
                shopping[item_id] = quantity
                montant = float(quantity * product.price)
                shopping[f"{item_id}_total"] = montant

                request.session['shopping'] = shopping
                request.session.modified = True

                if item_id in list(shopping.keys()):
                    messages.success(request, f'Updated {product.name} to {shopping[item_id]}')
                else:
                    messages.success(request, f'Added {product.name} to your shopping')
                
                print(request.session['shopping'])
    except Exception:
        messages.success(request, 'Erreur de quantité, vérifier et reéssayer')
    return redirect(redirect_url)

@login_required
def adjust_shopping_quantity(request, item_id):
    """Adjust the quantity of the specified product to the
    specified amount and display appropriate message"""
    if request.POST:
        try:
            product = Product.objects.get(pk=item_id)
        except Exception:
            product = None
            
        if product:
            shopping = request.session.get('shopping', {})
            quantity = int(request.POST.get('quantity'))
                
            if quantity > 0:
                shopping[item_id] = quantity
                messages.success(request, f'Updated {product.name} quantity to {shopping[item_id]}')
            else:
                shopping.pop(item_id)
                messages.success(request, f'Removed {product.name} from your shopping')
        else:
            messages.error(request, 'Erreur lors de la modification')

    request.session['shopping'] = shopping
    return redirect(reverse('view_shopping'))

@login_required
def adjust_shopping_discount(request):
    """Adjust user discount of the specified product to the
    specified amount and display appropriate message"""
    if request.POST:
        discount = float(request.POST.get('discount', 0.0))
        discount_type = request.POST.get('discount_type', 'percent')

        shopping = request.session.get('shopping', {})
        shopping['discount'] = discount
        shopping['discount_type'] = discount_type
        request.session['shopping'] = shopping
        messages.success(request, 'Mise à jour de la remise client bien effectuée')
    return redirect(reverse('view_shopping'))


@login_required
def remove_shopping_item(request, item_id):
    """Remove the item from the shopping and display appropriate message"""

    try:
        product = Product.objects.get(pk=item_id)
        if request.POST:
            shopping = request.session.get('shopping', {})

            shopping.pop(item_id)
            messages.success(request, f'Removed {product.name} from your shopping')

        request.session['shopping'] = shopping
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)

@login_required
def getAndSaveClientObject(request, employee, forceSave=False) -> (Client | None):
    client = None
    
    if request.method == 'POST':
        client_email = request.POST.get('client_email')
        client_phone_number = request.POST.get('client_phone_number')
        
        # Check if creating a new client
        if request.POST.get('sale_client') == 'new_client':
            # Try to find an existing client based on email or phone number
            try:
                client = Client.objects.get(Q(email=client_email) | Q(phone_number=client_phone_number))
            except Client.DoesNotExist:
                client = Client()  # Create a new client if none is found

        else:
            # Handle case for existing client selected via sale_client
            client_id = request.POST.get('sale_client')
            if client_id:
                try:
                    client = Client.objects.get(id=client_id)
                except Client.DoesNotExist:
                    client = Client()
            else:
                client = None

        if client:
            # Update the client's information
            client.first_name = request.POST.get('client_first_name')
            client.last_name = request.POST.get('client_last_name')
            client.email = client_email
            client.phone_number = client_phone_number
            client.phone_number_other = request.POST.get('client_phone_number_other')
            client.address = request.POST.get('client_address')
            client.country = request.POST.get('client_country')
            client.city = request.POST.get('client_city')
            client.company = request.POST.get('client_company')
            client.updated_by = employee
            client.updated_at = timezone.now()

            # Check if the checkbox for creating or updating the user is checked
            if request.POST.get('create_update_user') == 'on' or forceSave:
                create_permission = 'add_client'
                update_permission = 'change_client'
                # delete_permission = 'delete_client'
                # view_permission = 'view_client'
                
                if not has_perm(request.user, create_permission) or not has_perm(request.user, update_permission):
                    #raise PermissionDenied
                    messages.error(request, unAutorizedMsg)
                    return redirect(reverse('home'))
                client.save()

    return client

@login_required
def make_client_sale(request):
    if not request.session.get('shopping', {}):
        messages.error(request, "There's nothing in your shopping at the moment")
        return redirect(reverse('products'))
    
    create_permission = 'add_sale'
    # update_permission = 'change_sale'
    # delete_permission = 'delete_sale'
    view_permission = 'view_sale'
    
    create_item_permission = 'add_saleitem'
    # update_item_permission = 'change_saleitem'
    # delete_item_permission = 'delete_saleitem'
    # view_item_permission = 'view_saleitem'
    
    create_payment_permission = 'add_payment'
    # update_payment_permission = 'change_payment'
    # delete_payment_permission = 'delete_payment'
    # view_payment_permission = 'view_payment'
    
        
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))

    if request.method == 'POST':
        rpg = request.POST.get
        try:
            current_user = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            current_user = None
             
        if current_user:
            client = getAndSaveClientObject(request, current_user, forceSave=True)
            if client:
                shopContents = shopping_contents(request)
                totalHT = Decimal(shopContents['totalHT']) if shopContents and 'totalHT' in shopContents and shopContents['totalHT'] > 0 else None
                
                payment_date = parseDatetime(rpg('payment_date')) if notEmpty(rpg('payment_date')) else ''
                payment_due_date = parseDatetime(rpg('payment_due_date')) if notEmpty(rpg('payment_due_date')) else timezone.now()
                tax_rate = safeDecimal(rpg('client_tax_rate')) if rpg('apply_tax') == 'on' and notEmpty(rpg('client_tax_rate')) else Decimal('0')
                payment_status = rpg('client_payment_status')
                payment_method = rpg('client_payment_method')
                
                if shopContents['discount_type'] == 'percent' or shopContents['discount_type'] == 'percent_small':
                    saleTTC = float(totalHT) + (float(totalHT) * givenRate(tax_rate))
                    discount = Decimal(saleTTC * givenRate(shopContents['discount'])) if saleTTC and saleTTC >= 0 and notEmpty(shopContents['discount']) and shopContents['discount'] > 0 else Decimal('0')
                else:
                    discount = Decimal(shopContents['discount']) if shopContents and 'discount' in shopContents and shopContents['discount'] >= 0 else Decimal('0')
            
                if totalHT:
                    if not has_perm(request.user, create_permission):
                        #raise PermissionDenied
                        messages.error(request, unAutorizedMsg)
                        return redirect(reverse('home'))
                    
                    sale = Sale(user=current_user, client=client)
                    sale.discount=discount
                    sale.ht_amount=totalHT
                    sale.tax_rate=tax_rate
                    sale.payment_due_date=payment_due_date
                    sale.created_at = timezone.now()
                    sale.save()
                    
                    makePayment = False
                    paidAmount = 0
                    
                    if payment_status == 'paid_in_total':
                        makePayment = True
                        paidAmount = sale.ttc_amount
                    elif payment_status == 'paid_in_part':
                        makePayment = True
                        paidAmount = Decimal(rpg('client_payment_amount')) if notEmpty(rpg('client_payment_amount')) else Decimal('0')
                    
                    items = []
                    payments = []
                    
                    try:
                        for shop in shopContents['shopping_items']:
                            product = Product.objects.get(id=shop['item_id'])
                            items.append(SaleItem(sale=sale, product=product, user=current_user, quantity=shop['quantity'], price=product.price))
                        
                        if makePayment:
                            payments.append(Payment(sale=sale, user=current_user, amount=paidAmount, date=payment_date, method=payment_method, status=payment_status))
                
                        deleteShoppingData = False

                        if len(items) > 0 :
                            if not has_perm(request.user, create_item_permission):
                                #raise PermissionDenied
                                messages.error(request, unAutorizedMsg)
                                return redirect(reverse('home'))
                            deleteShoppingData = True
                            SaleItem.objects.bulk_create(items)
                            
                        if len(payments) > 0 :
                            if not has_perm(request.user, create_payment_permission):
                                #raise PermissionDenied
                                messages.error(request, unAutorizedMsg)
                                return redirect(reverse('home'))
                            Payment.objects.bulk_create(payments)
                            
                        if deleteShoppingData:
                            if 'shopping' in request.session:
                                del request.session['shopping']
                                
                        messages.success(request, 'Vente effectuée avec succès!')
                        return redirect('sale_success', sale_id=sale.id)
                        
                    except Exception:
                        messages.error(request, (
                            "Problème avec votre base de données"
                            "Contacter l'administrateur")
                        )
                        sale.delete()
                        return redirect(reverse('view_shopping'))
            else:
                messages.error(request, 'Une erreur s\'est produite avec le client, veuillez reesayer!')         
        else:
            messages.error(request, 'Une erreur s\'est produite, veuillez reesayer!')
    else:
        return redirect(reverse('view_shopping'))

@login_required
def sale_make_rest_payment(request, sale_id):
    create_permission = 'add_payment'
    # update_permission = 'change_payment'
    # delete_permission = 'delete_payment'
    view_permission = 'view_payment'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        rpg = request.POST.get
        try:
            current_user = Employee.objects.get(user=request.user)
            sale = Sale.objects.get(id=sale_id)
        except Exception:
            current_user = None
            sale = None
             
        if current_user and sale:
            payment_date = parseDatetime(rpg('payment_date')) if notEmpty(rpg('payment_date')) else ''
            payment_status = rpg('client_payment_status')
            payment_method = rpg('client_payment_method')
            paidAmount = Decimal(rpg('client_payment_amount')) if notEmpty(rpg('client_payment_amount')) else Decimal('0')
            try:
                if not has_perm(request.user, create_permission):
                    #raise PermissionDenied
                    messages.error(request, unAutorizedMsg)
                    return redirect(reverse('home'))
                
                payment = Payment(sale=sale, user=current_user, amount=paidAmount, date=payment_date, method=payment_method, status=payment_status)
                payment.save()
                messages.success(request, 'Paiement effectué avec succès!')
            except Exception:
                messages.error(request, 'Problème lors de la sauvegarde')
        else:
            messages.error(request, 'Une erreur s\'est produite, veuillez reesayer!')
    return redirect(reverse('admin_list_sales'))

@login_required
def print_sale(request, sale_id):
    # create_permission = 'add_sale'
    # update_permission = 'change_sale'
    # delete_permission = 'delete_sale'
    view_permission = 'view_sale'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        rpg = request.POST.get
        sale = None
        sale_items = []  
        shopContents = shopping_contents(request)  
        employee = None
        client = None
        totalHT = None
        discount = None
        sale_date = timezone.now()
        
        paidAmount = 0
        
        try:
            employee = Employee.objects.get(user=request.user) if request.user.is_authenticated else None
            
            if sale_id == 'sale_proformat':
                client = getAndSaveClientObject(request, employee)
                totalHT = Decimal(shopContents['totalHT']) if shopContents and 'totalHT' in shopContents and shopContents['totalHT'] > 0 else None
                payment_due_date = parseDatetime(rpg('payment_due_date')) if notEmpty(rpg('payment_due_date')) else timezone.now
                tax_rate = safeDecimal(rpg('client_tax_rate')) if rpg('apply_tax') == 'on' and notEmpty(rpg('client_tax_rate')) else Decimal('0')
                payment_status = rpg('client_payment_status')
                
                if shopContents['discount_type'] == 'percent' or shopContents['discount_type'] == 'percent_small':
                    saleTTC = float(totalHT) + (float(totalHT) * givenRate(tax_rate))
                    discount = Decimal(saleTTC * givenRate(shopContents['discount'])) if saleTTC and saleTTC >= 0 and notEmpty(shopContents['discount']) and shopContents['discount'] > 0 else Decimal('0')
                else:
                    discount = Decimal(shopContents['discount']) if shopContents and 'discount' in shopContents and shopContents['discount'] >= 0 else Decimal('0')
            
                
                # payment_date = parseDatetime(rpg('payment_date')) if notEmpty(rpg('payment_date')) else ''
                # payment_method = rpg('client_payment_method')
                if employee and client and totalHT:
                    sale = Sale(user=employee, client=client, discount=discount, ht_amount=totalHT, date=sale_date, tax_rate=tax_rate, payment_due_date=payment_due_date)
                    for item in shopContents['shopping_items']:
                        product = Product.objects.get(id=item['item_id'])
                        
                        # for i in range(1, 50):
                        #     # print(i)
                        sale_items.append(SaleItem(sale=sale, product=product, quantity=item['quantity'], price=product.price))
                        
            
                if payment_status == 'paid_in_total':
                    if sale:
                        paidAmount = sale.ttc_amount
                elif payment_status == 'paid_in_part':
                    paidAmount = Decimal(rpg('client_payment_amount')) if notEmpty(rpg('client_payment_amount')) else Decimal('0')
            else:
                try:
                    sale = Sale.objects.get(id=sale_id)
                    sale_items = sale.items
                    # paidAmount = sale.ttc_amount
                    paidAmount = sale.payments_amount
                except Exception:
                    pass
                        
            if sale and len(sale_items) > 0:
                # arguments = {'is_proformat': True, 'save_pdf_file': True, 'download_sale_pdf': True, client_sale_email='client@example.com'}
                # arguments = {'client_sale_email': client.email}
                arguments = {}
                
                return generate_sale_pdf(sale, sale_items, paidAmount, arguments)
            else:
                messages.error(request, 'Erreur-A lors de la génération de la facture')
                return redirect(reverse('view_shopping'))
        except Exception as e:
            messages.error(request, f'Erreur-B: {e}')
            return redirect(reverse('view_shopping'))
    else:
        messages.error(request, 'Erreur-C lors de la génération de la facture')
        return redirect(reverse('view_shopping'))

@login_required
def update_sale_item_view(request, item_id):
    # create_permission = 'add_saleitem'
    update_permission = 'change_saleitem'
    # delete_permission = 'delete_saleitem'
    view_permission = 'view_saleitem'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        try:
            if not has_perm(request.user, update_permission):
                #raise PermissionDenied
                messages.error(request, unAutorizedMsg)
                return redirect(reverse('home'))
            
            try:
                current_user = Employee.objects.get(user=request.user)
            except Exception:
                current_user = None
            
            saleItem = SaleItem.objects.get(id=item_id)
            saleItem.observation = request.POST.get('observation')
            saleItem.updated_by = current_user
            saleItem.updated_at = timezone.now()
            saleItem.save()
        except Exception:
            pass
        
    return redirect(reverse('admin_list_sales'))

@login_required
def bordereau_livraison_view(request, sale_id):
    # create_permission = 'add_sale'
    # update_permission = 'change_sale'
    # delete_permission = 'delete_sale'
    view_permission = 'view_sale'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    try:
        base64_file_path = os.path.join(settings.MEDIA_ROOT, 'logo_base64.txt')
        base64_string = read_base64_file(base64_file_path)
        output_format = request.GET.get('format') # 'pdf' or 'print'

        MAX_ITEMS_PER_PAGE1 = 18
        MAX_ITEMS_PER_PAGE2 = 24
    
        sale = Sale.objects.get(id=sale_id)
        sale_items = sale.items
            
        items_pages = []
        i = 0
        while i < len(sale_items):
            if len(items_pages) == 0:
                max_items_per_page = MAX_ITEMS_PER_PAGE1
            else:
                max_items_per_page = MAX_ITEMS_PER_PAGE2
            items_pages.append(sale_items[i:i + max_items_per_page])
            i += max_items_per_page


        try:
            app_site = AppSite.objects.get(site__id=1)
        except Exception:
            app_site = {}
            
        context = {
            'date': timezone.now().strftime('%d/%m/%Y à %H:%m'),
            'sale': sale,
            'items_pages': items_pages,
            'second_last_index': len(items_pages),
            'base64_string': base64_string,
            'output_format': output_format,
            'app_site': app_site,
        }
        
        if output_format == 'pdf':
            html_content = render_to_string('sales/bordereau_livraison.html', context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="bordereau_livraison.pdf"'
            page_size = 'A4'
            orientation = 'portrait'
            css_string = f"""
                @page {{
                    size: {page_size} {orientation};
                    margin: 1.5cm;
                }}

                body {{
                    font-family: Arial, sans-serif;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}

                th, td {{
                    padding: 10px;
                    border: 1px solid #ddd;
                }}

                th {{
                    background-color: #f4f4f4;
                }}
            """
            HTML(string=html_content).write_pdf(response, stylesheets=[CSS(string=css_string)])

            return response
        
        return render(request, 'sales/bordereau_livraison.html', context)

    except Exception:
        return redirect('admin_list_sales')

def generate_sale_pdf(sale, sale_items, paidAmount, args={}):
    """ args = {is_proformat = False, download_sale_pdf=False, save_pdf_file = False} """
    
    base64_file_path = os.path.join(settings.MEDIA_ROOT, 'logo_base64.txt')
    base64_string = read_base64_file(base64_file_path)

    MAX_ITEMS_PER_PAGE1 = 18
    MAX_ITEMS_PER_PAGE2 = 24

    items_pages = []
    i = 0
    while i < len(sale_items):
        if len(items_pages) == 0:
            max_items_per_page = MAX_ITEMS_PER_PAGE1
        else:
            max_items_per_page = MAX_ITEMS_PER_PAGE2
        items_pages.append(sale_items[i:i + max_items_per_page])
        i += max_items_per_page

    try:
        app_site = AppSite.objects.get(site__id=1)
    except Exception:
        app_site = {}

    # Page settings
    page_size = 'A4'
    orientation = 'portrait'
    css_string = f"""
    @page {{
        size: {page_size} {orientation};
        margin: 1.5cm;
    }}
    """
    
    sale_name = 'Facture-Proformat N°' if args.get('is_proformat', False) else 'Facture N°'

    # Render the sale as HTML
    html_string = render_to_string('sales/sale_print.html', {
        'sale': sale,
        'items_pages': items_pages,
        'second_last_index': len(items_pages),
        'base64_string': base64_string,
        'app_site': app_site,
        'paidAmount': float(paidAmount),
        'unPaidAmount': sale.ttc_amount - float(paidAmount),
        'sale_name': sale_name,
        'price_unit': 'FCFA'
    })

    html = HTML(string=html_string)
    pdf = html.write_pdf(stylesheets=[CSS(string=css_string)])

    # Save PDF to file (temporary location)
    output_filename = f"facture-{sale.invoice_number}.pdf"
    output_path = os.path.join(settings.MEDIA_ROOT, 'factures', output_filename)
    
    if args.get('save_pdf_file', False):
        save_pdf_file(output_path, pdf)
        
    # Create the response for download if required
    response = HttpResponse(pdf, content_type='application/pdf')
    if args.get('download_sale_pdf', False):
        response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
    else:
        response['Content-Disposition'] = f'filename="{output_filename}"'

    # If client email is provided, send the email with the PDF attachment
    client_email = args.get('client_sale_email')
    if notEmpty(client_email):
        save_pdf_file(output_path, pdf)
            
        email_subject = f'Votre {sale_name} de chez {app_site.name}'
        email_body = f'Salut {sale.client.full_name},\n\nVeuillez trouver ci-joint votre {sale_name} n°{sale.invoice_number}.\n\nMerci !\n\n\n{app_site.name}\n{app_site.email}\n{app_site.phone_number}\n{app_site.address}'
        send_email_with_attachment(client_email, email_subject , email_body, output_path)
    return response

@login_required
def sale_success(request, sale_id):
    """
    Handle successful sale
    """
    try:
        sale = Sale.objects.get(id=sale_id)
        sale_items = sale.items
        paidAmount = sale.payments_amount
                        
        if sale and len(sale_items) > 0:
            arguments = {}
            return generate_sale_pdf(sale, sale_items, paidAmount, arguments)
        # else:
        #     messages.error(request, 'Erreur: lors de la génération de la facture')
        #     return redirect(reverse('view_shopping'))
    except Exception:
        messages.error(request, 'Erreur lors de la vente!')

    return render(request, 'sales/sale_success.html', { 'sale': sale })

@login_required
def payroll_dashboard(request):
    # create_permission = 'add_payroll'
    # update_permission = 'change_payroll'
    # delete_permission = 'delete_payroll'
    view_permission = 'view_payroll'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    # Retrieve the year from the query parameters or default to the current year
    year = int(request.POST.get('year', date.today().year))  # Ensure year is an integer
    employees = Employee.objects.filter(user__is_superuser=False, deleted=False)

    # Define month abbreviations for easier mapping
    months = {
        1: 'jan',
        2: 'fev',
        3: 'mar',
        4: 'avr',
        5: 'mai',
        6: 'jui',
        7: 'jul',
        8: 'aou',
        9: 'sep',
        10: 'oct',
        11: 'nov',
        12: 'dec',
    }

    # Prepare a list to hold salary data for each employee
    salaries = []
    monthsRange = range(1, 13)

    # Iterate through each employee to calculate their monthly salaries
    for employee in employees:
        monthly_salaries = {'employee': employee}
        for month in monthsRange:  # Loop through months 1 to 12
            # Filter Payroll records for the current employee, month, year, and not deleted
            total_net_salary = Payroll.objects.filter(
                employee=employee,
                date__month=month,
                date__year=year,
                deleted=False
            ).aggregate(total=Sum('salary_net'))['total'] or 0
            
            # Store the total salary in the corresponding month key
            monthly_salaries[months[month]] = total_net_salary
        global_sum = sum(monthly_salaries[months[m]] for m in monthsRange)
        
        if global_sum > 0:
            salaries.append(monthly_salaries)
        
    years = get_years_list()

    # Prepare context for rendering the template
    context = {
        'salaries': salaries,
        'year': year,
        'years': years
    }

    return render(request, 'dashboards/payroll_dashboard.html', context)

@login_required
def sale_dashboard(request):
    # create_permission = 'add_sale'
    # update_permission = 'change_sale'
    # delete_permission = 'delete_sale'
    view_permission = 'view_sale'
    
    if not has_perm(request.user, view_permission):
        #raise PermissionDenied
        messages.error(request, unAutorizedMsg)
        return redirect(reverse('home'))
    
    # Retrieve the year from the query parameters or default to the current year
    year = int(request.POST.get('year', date.today().year))  # Ensure year is an integer

    clients = Client.objects.filter(deleted=False)
    
    # Define month abbreviations for easier mapping
    months = {
        1: 'jan',
        2: 'fev',
        3: 'mar',
        4: 'avr',
        5: 'mai',
        6: 'jui',
        7: 'jul',
        8: 'aou',
        9: 'sep',
        10: 'oct',
        11: 'nov',
        12: 'dec',
    }
    
    sales = []
    monthsRange = range(1, 13)
    
    for client in clients:
        monthly_sales= {'client': client}
        for month in monthsRange:
            sales_filter = Sale.objects.filter(
                client=client,
                date__month=month,
                date__year=year,
                deleted=False
            )
            total_sales = sum(sale.ttc_amount for sale in sales_filter) if len(sales_filter) > 0 else 0
            monthly_sales[months[month]] = total_sales
        
        global_sum = sum(monthly_sales[months[m]] for m in monthsRange)
        if global_sum > 0:
            sales.append(monthly_sales)
        
    years = get_years_list()
    
    context = {
        'sales': sales,
        'year': year,
        'years': years,
    }

    return render(request, 'dashboards/sale_dashboard.html', context)

