import json
import uuid
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from webview.functions import users_pictures_path, users_pictures_path_thumb, products_pictures_path
from django.core.files.storage import default_storage as storage
from decimal import Decimal
from webview.utils import notEmpty
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.contrib.sites.models import Site

from django.db.models import Q

default_user_icon="default-user-icon.png"
no_image_available="no-image-available.png"

class AppSite(models.Model):
    id = models.PositiveIntegerField(primary_key=True, null=False, blank=False)
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='app_site')
    email = models.EmailField(unique=True, null=False, blank=False)
    owner_email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=254, null=False, blank=False)
    phone_number_other = models.CharField(max_length=254, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(default=False, null=False, blank=False)

    # Constants (No commas at the end)
    NAME = 'KnelCare'
    DOMAIN = 'knelcare.com'
    EMAIL = 'knelcare@knelcare.com'
    PHONE1 = '+228 92645651'
    PHONE2 = '+228 98284737'
    ADDRESS = '400 BP 351, Angle Rues Hôtel Léota et Hôtel de France, Quartier Lama, Kara'

    @property
    def name(self):
        return self.site.name

    @property
    def domain(self):
        return self.site.domain

    class Meta:
        verbose_name = 'App Site'
        verbose_name_plural = 'App Sites'

    def __str__(self):
        return self.site.name

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254, unique=True, null=False, blank=False)
    tax = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False, default=Decimal('0'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_countries', null=True, blank=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_countries', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_countries', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    deleted = models.BooleanField(default=False, null=False, blank=False)
    
    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

class Role(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True, null=False, blank=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles', null=True, blank=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_roles', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_roles', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    deleted = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return self.name

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_employees')
    salary_base = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    # country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    phone_number = models.CharField(unique=True, max_length=20, null=True, blank=True)
    employee_pic = models.ImageField(upload_to=users_pictures_path, null=True, blank=True)
    employee_pic_thumb = models.ImageField(upload_to=users_pictures_path_thumb, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_verified = models.BooleanField(default=False, blank=True)
    agree_privacy_policy = models.BooleanField(default=False, null=False, blank=False)
    roles = models.ManyToManyField(Role, related_name='roles_employees', blank=True, default='user')
    # roles = models.CharField(max_length=255, null=True, blank=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_employees', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_employees', null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    deleted = models.BooleanField(default=False, null=False, blank=False)
    
    @property
    def permissions_ids(self):
        return list(self.user.user_permissions.values_list('id', flat=True))
    
    @property
    def permissions_codenames(self):
        return list(self.user.user_permissions.values_list('codename', flat=True))
    @property
    def toMap(self):
        mapData = {
            'id': self.id,
            'user': self.user.id if self.user else None,
            'username': self.user.username if self.user else '',
            'first_name': self.user.first_name if self.user else '',
            'last_name': self.user.last_name if self.user else '',
            'full_name': self.full_name,
            'salary_base': float(self.salary_base),
            'email': self.user.email if self.user else '',
            # 'country': self.country.id if self.country else None,
            'roles': self.list_roles(),
            'phone_number': self.phone_number,
            'is_active': self.user.is_active,
            'biography': self.biography,
            'location': self.location,
            'birth_date': self.birth_date.strftime('%Y-%m-%d') if self.birth_date else None,
            'agree_privacy_policy': self.agree_privacy_policy,
            'employee_pic': self.employee_pic.url if self.employee_pic else None,
            'employee_pic_thumb': self.employee_pic_thumb.url if self.employee_pic_thumb else None,
            'permissions_ids': self.permissions_ids,
        }
        
        return json.dumps(mapData)
    @property
    def imageUrl(self):
        """
        Returns the image URL if the image_url field is not empty.
        Otherwise, returns the URL of the ImageField if an image is uploaded.
        """
        if notEmpty(self.employee_pic):
            return self.employee_pic.url
        elif notEmpty(self.employee_pic_thumb):
            return self.employee_pic_thumb.url
        # return f'{ settings.MEDIA_URL }images/{default_user_icon}'
        return f'images/{default_user_icon}'
    @property
    def full_name(self):
        if notEmpty(self.user.first_name) or notEmpty(self.user.last_name):
            return f'{self.user.first_name} {self.user.last_name}'
        else:
            return f'{self.user.username}'
        


    @property
    def isAdmin(self):
        return self.has_role('admin')
    
    @property
    def isPayrollUser(self):
        return self.has_role('user_payroll')
    
    @property
    def isDashboardUser(self):
        return self.has_role('dashboard')
    
    @property
    def small_picture(self):
        if notEmpty(self.employee_pic_thumb):
            return self.employee_pic_thumb.url
        # return f'{ settings.MEDIA_URL }images/{default_user_icon}'
        return f'images/{default_user_icon}'
    @property
    def large_picture(self):
        if notEmpty(self.employee_pic):
            return self.employee_pic.url
        # return f'{ settings.MEDIA_URL }images/{default_user_icon}'
        return f'images/{default_user_icon}'
    
    def save(self, *args, **kwargs):
        if self.user and not self.id:
            self.id = self.user.id
            
        super(Employee, self).save(*args, **kwargs)
        
        if self.employee_pic:
            img = Image.open(self.employee_pic.path)
            if img.height > 300 or img.width > 300:
                img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.employee_pic.path)

        if self.employee_pic_thumb:
            img_thumb = Image.open(self.employee_pic_thumb.path)
            if img_thumb.height > 50 or img_thumb.width > 50:
                img_thumb = img_thumb.resize((50, 50), Image.LANCZOS)
            img_thumb.save(self.employee_pic_thumb.path)
    def delete(self, *args, **kwargs):
        if self.employee_pic and not self.employee_pic.name.endswith(default_user_icon):
            if storage.exists(self.employee_pic.path):
                storage.delete(self.employee_pic.path)

        if self.employee_pic_thumb and not self.employee_pic_thumb.name.endswith(default_user_icon):
            if storage.exists(self.employee_pic_thumb.path):
                storage.delete(self.employee_pic_thumb.path)

        super(Employee, self).delete(*args, **kwargs)
    def has_role(self, role_name):
        """
        Check if the user has a specific role.
        """
        return self.roles.filter(Q(id=role_name) | Q(name=role_name), deleted=False).exists()
    def list_roles(self):
        # Returns a comma-separated string of role names
        return ", ".join([r.id for r in self.roles.filter(deleted=False)])
    def list_roles_name(self):
        # Returns a comma-separated string of role names
        return ", ".join([role.name for role in self.roles.filter(deleted=False)])

    list_roles.short_description = 'Roles'
    
    # def __str__(self):
    #     return f'{self.user.username} with roles: {", ".join([role.name for role in self.roles.filter(deleted=False)])}'
    
    def __str__(self):
        fName = self.user.first_name
        lName = self.user.last_name
        return  f'{fName} {lName}' if notEmpty(fName) or notEmpty(lName) else self.user.username

class Payroll(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    salary_base = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    deleted = models.BooleanField(default=False, null=False, blank=False)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='payrolls')
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='updated_payrolls', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    
    @property
    def toMap(self):
        mapData = {
            'id': self.id,
            'employee': self.employee.id if self.employee else None,
            'username': self.employee.user.username if self.employee and self.employee.user else '',
            'first_name': self.employee.user.first_name if self.employee and self.employee.user else '',
            'last_name': self.employee.user.last_name if self.employee and self.employee.user else '',
            'full_name': self.employee.full_name,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'salary_base': float(self.salary_base),
            'commission': float(self.commission) if self.commission and self.commission > 0 else 0.0,
        }
        
        return json.dumps(mapData)
    
    
    @property
    def total_salary(self):
        return float(self.salary_base) + float(self.commission)
    
    def __str__(self):
        return f"Paie de {self.employee} pour {self.date.strftime('%B %Y')}"

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='clients')
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(unique=True, max_length=20, null=False, blank=False)
    phone_number_other = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    # country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    loyalty_point = models.IntegerField(default=0)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_clients', null=True, blank=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='updated_clients', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    deleted = models.BooleanField(default=False, null=False, blank=False)
    
    @property
    def toMap(self):
        return json.dumps({
            'id': self.id,
            'user': self.user.id if self.user else None,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'phone_number_other': self.phone_number_other,
            'address': self.address,
            'country': self.country,
            'city': self.city,
            'company': self.company,
            'loyalty_point': self.loyalty_point,
        })

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='categories')
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    # created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='created_categories', null=True, blank=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='updated_categories', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    deleted = models.BooleanField(default=False, null=False, blank=False)
    
    @property
    def toMap(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'description': self.description,
        })
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='user_products')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    # stock = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=254, null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    is_available = models.BooleanField(default=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to=products_pictures_path, null=True, blank=True, default=f"images/{no_image_available}")
    # created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='created_products', null=True, blank=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='updated_products', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    deleted = models.BooleanField(default=False, null=False, blank=False)
    
    @property
    def toMap(self):
        return json.dumps({
            'id': self.id,
            'category': self.category.id if self.category else None,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'is_available': self.is_available,
            'image_url': self.image_url,
            'image': self.image.url if self.image else None,
            'imageUrl': self.imageUrl,
        })
        
    @property
    def utils(self):
        sales = SaleItem.objects.filter(product=self, deleted=False)
        stocks = Stock.objects.filter(product=self, deleted=False)
        
        salesQties = sum(sale.quantity for sale in sales) if sales and len(sales) > 0 else 0
        stockQties = sum(stock.quantity for stock in stocks) if stocks and len(stocks) > 0 else 0
        
        salesAmounts = sum(sale.amount for sale in sales) if sales and len(sales) > 0 else Decimal('0')
        stockAmounts = sum(stock.amount for stock in stocks) if stocks and len(stocks) > 0 else Decimal('0')

        return {
            'available_stock': stockQties - salesQties,
            'profit': salesAmounts - stockAmounts
        }
   
    @property
    def isAvailable(self):
        return 'Disponible' if self.is_available else 'Indisponible'
        
    @property
    def imageUrl(self):
        """
        Returns the image URL if the image_url field is not empty.
        Otherwise, returns the URL of the ImageField if an image is uploaded.
        """
        if notEmpty(self.image_url):
            return self.image_url
        elif notEmpty(self.image):
            return self.image.url
        # return f'{ settings.MEDIA_URL }images/{no_image_available}'
        return f'images/{no_image_available}'
    
    def __str__(self):
        return self.name

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='user_stocks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False, related_name='product_stocks')
    quantity = models.PositiveIntegerField(null=False, blank=False, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    amount = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False, editable=False)
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='updated_stocks')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    deleted = models.BooleanField(default=False, null=False, blank=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.quantity and self.price:
            self.amount = Decimal(self.quantity) * self.price
    
    @property
    def toMap(self):
        return json.dumps({
            'id': self.id,
            'product': self.product.id if self.product else None,
            'quantity': self.quantity,
            'price': float(self.price),
        })
       

    def save(self, *args, **kwargs):
        """
        Override the save method to calculate and set the total amount based on
        quantity and the sale price from the related StockLot.
        """
        # Utiliser le prix de vente du lot pour calculer le montant
        if not self.amount:
            self.amount = Decimal(self.quantity) * self.price
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.price}"

class Sale(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True, null=False, blank=False)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='user_sales')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_sales')
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=20, decimal_places=2, default=0, editable=False)
    ht_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    payment_due_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='updated_sales', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, null=False, blank=False)
    # payment_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    # commission_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Commission en pourcentage")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = self._generate_order_number()
 
    def _generate_order_number(self):
        """
        Generate a unique order number using user ID, client ID, and a UUID for randomness.
        """
        return f'{self.user.id}-{self.client.id}-{uuid.uuid4().hex[:8]}'

    @property
    def toMap(self):
        return {
            'id': self.id,
            'user': self.user,
            'client': self.client,
            'discount': self.discount,
            'tax_rate': self.tax_rate,
            'ht_amount': self.ht_amount,
            'ttc_amount': self.ttc_amount,
            'payments_amount': float(self.payments_amount),
            'restToPay': self.restToPay,
            'payment_due_date': self.payment_due_date,
            'updated_by': self.updated_by,
            'created_at': self.created_at,
            'updated_at': self.updated_at, 
        }
        
    # @property 
    # def commission(self):
    #     return (self.amount * self.commission_rate) / Decimal('100')
        
    @property
    def tax_amount(self):
        taxRateBrut = (float(self.tax_rate) if self.tax_rate is not None and self.tax_rate > 0 else 0.0)
        taxRate = (taxRateBrut / 100) if taxRateBrut > 1 else taxRateBrut
        return (float(self.ht_amount) * taxRate)
    
    @property
    def ttc_amount(self):
        return (float(self.ht_amount) + self.tax_amount) - float(self.discount)
    
    @property
    def items(self):
        """
        Retrieve the items for this sale from the SaleItem table.
        """
        return SaleItem.objects.filter(sale=self, deleted=False) if self.id else []
        
    @property
    def payments(self):
        """
        Retrieve the items for this sale from the SaleItem table.
        """
        return Payment.objects.filter(sale=self, deleted=False) if self.id else []
    
    @property
    def itemsToMap(self):
        iMaps = []
        for i in self.items:
            iMaps.append({ 'id': i.id, 'product': i.product.toMap, 'quantity': i.quantity, 'price': float(i.price), 'amount': float(i.amount) })
        return json.dumps(iMaps)
    
    @property
    def paymentsToMap(self):
        pMaps = []
        for p in self.payments:
            pMaps.append({ 'id': p.id, 'amount': float(p.amount), 'date': p.date.isoformat() if p.date else '', 'method': self.getMethod(p.method) })
        return json.dumps(pMaps) 
    
    @property
    def restToPay(self):
        return self.ttc_amount - float(self.payments_amount)
    
    def getMethod(self, method):
        if method == 'card':
            return 'Carte Bancaire'
        elif method == 'transfer':
            return 'Virement'
        elif method == 'cash':
            return 'Espèces'
        else:
            return ''
    
    @property
    def payments_amount(self):
        amount = sum(pay.amount for pay in self.payments) if self.payments and len(self.payments) > 0 else 0
        return amount
    
    @property
    def is_paid(self) -> bool:
        amount = self.payments_amount
        amountTTC = self.ttc_amount
        if amountTTC and amountTTC > 0:
            if amount and amount >= amountTTC:
                return True
        return False
    
    @property
    def status(self) -> dict[str, str]:
        amount = self.payments_amount
        amountTTC = self.ttc_amount
        
        # Convert `payment_due_date` to string and parse it for comparison
        parsed_payment_due_date = parse_datetime(f'{self.payment_due_date}')
        
        if amountTTC and amountTTC > 0:
            if amount and amount >= amountTTC:
                return {'id': 'paid', 'name': 'Payée', 'class': 'success'}
            elif parsed_payment_due_date and parsed_payment_due_date > timezone.now():
                return {'id': 'pending', 'name': 'En cours', 'class': 'warning'}
            else:
                return {'id': 'overdue', 'name': 'En retard', 'class': 'danger'}
        else:
            return {'id': '', 'name': '', 'class': ''}
    
    def save(self, *args, **kwargs):
        """
        Override the save method to ensure id and totals are set properly.
        """
        if not self.id:
            self.id = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vente {self.id} par {self.user} pour {self.client}"

class SaleItem(models.Model):
    id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, related_name='sale_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False, related_name='sale_items')
    quantity = models.PositiveIntegerField(null=False, blank=False, default=0)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0, editable=False)
    observation = models.TextField(blank=True, null=False)
    deleted = models.BooleanField(default=False, null=False, blank=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.amount = Decimal(self.quantity) * self.price
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.price}"

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_payments')
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='user_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    date = models.DateTimeField(default=timezone.now)
    method_choices = [
        ('card', 'Carte Bancaire'), 
        ('transfer', 'Virement'), 
        ('cash', 'Espèces')
    ]
    method = models.CharField(max_length=10, choices=method_choices, null=False, blank=False, default='cash')
    payment_status_choices = [
        ('paid_in_total', 'Payé en totalité'), 
        ('paid_in_part', 'Payé en partie'), 
        ('unpaid', 'Non Payé')
    ]
    status = models.CharField(max_length=20, choices=payment_status_choices, null=False, blank=False, default='unpaid')
    # created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='created_payments', null=True, blank=True)
    updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='updated_payments', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    deleted = models.BooleanField(default=False, null=False, blank=False)
    
    def __str__(self):
        return f"Payment of {self.amount} for Sale {self.sale.id}"

# class LoyaltyHistory(models.Model):
#     id = models.AutoField(primary_key=True)
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='loyalty_histories')
#     points_earned = models.IntegerField()
#     points_spent = models.IntegerField(default=0)
#     date = models.DateTimeField(auto_now_add=True)
#     description = models.TextField(blank=True)
#     # created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='created_loyalty_histories', null=True, blank=True)
#     updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='updated_loyalty_histories', null=True, blank=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
#     deleted = models.BooleanField(default=False, null=False, blank=False)
    
#     class Meta:
#         verbose_name_plural = 'LoyaltyHistories'

#     def __str__(self):
#         return f"{self.points_earned} points for {self.client.name} on {self.date}"

# class StockLot(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=254, null=False)
#     created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
#     updated_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)

#     def __str__(self):
#         return self.name