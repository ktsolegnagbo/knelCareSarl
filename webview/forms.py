# accounts/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Category, Client, Employee, ExpiredStock, Product, Stock
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Display permissions as checkboxes
        required=False,
        label="Permissions",
    )
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Display users as checkboxes
        required=False,
        label="Assign Users to Group",
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions', 'users']
        labels = {
            'name': 'Group Name',
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom de la categorie',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                # 'cols': 20,
                'rows': 2,
                'placeholder': 'Entrez la description ici...',
            }),
        }
        labels = {
            'name': 'Nom de la categorie',
            'description': 'Description de la categorie',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir les champs requis
        self.fields['name'].required = True
        self.fields['description'].required = False
    
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'alert_threshold', 'is_available', 'image_url', 'image']
        
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
                'empty_label': 'Sélectionnez une catégorie',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom du produit',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                # 'cols': 20,
                'rows': 2,
                'placeholder': 'Entrez la description du produit ici...',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Entrez le prix du produit',
            }),
            'alert_threshold': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1',
                'placeholder': 'Entrez le seuil d\'alerte',
            }),
            
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez l\'URL de l\'image',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }
        
        labels = {
            'category': 'Catégorie du produit',
            'name': 'Nom du produit',
            'description': 'Description du produit',
            'price': 'Prix de vente du produit',
            'alert_threshold': 'Seuil d\'alerte Quantité',
            'is_available': 'Disponibilité du produit',
            'image_url': 'URL de l\'image',
            'image': 'Image du produit',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir les champs requis
        self.fields['category'].required = True
        self.fields['name'].required = True
        self.fields['description'].required = False
        self.fields['price'].required = True
        self.fields['alert_threshold'].required = True
        self.fields['image_url'].required = False
        self.fields['image'].required = False

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['product', 'quantity', 'price', 'expiration_date']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'empty_label': 'Sélectionnez un produit',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1',
                'placeholder': 'Entrez la quantité du stock',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Entrez le prix d\'achat du produit',
            }),
            'expiration_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choisir date de péromption',
                'type': 'date'
            }),
        }
        labels = {
            'product': 'Nom du produit',
            'quantity': 'Entrer La Quantité du stock',
            'price': 'Prix d\'achat du produit',
            'expiration_date': 'Date de péromption',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir les champs requis
        self.fields['product'].required = True
        self.fields['quantity'].required = True
        self.fields['price'].required = True
        self.fields['expiration_date'].required = True
        
class ExpiredStockForm(forms.ModelForm):
    class Meta:
        model = ExpiredStock
        fields = ['product', 'quantity', 'expiration_date']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'empty_label': 'Sélectionnez un produit',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1',
                'placeholder': 'Entrez la quantité Périmée',
            }),
            'expiration_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choisir date de péromption',
                'type': 'date'
            }),
        }
        labels = {
            'product': 'Nom du produit',
            'quantity': 'Entrer La Quantité Périmée',
            'expiration_date': 'Date de péromption',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir les champs requis
        self.fields['product'].required = True
        self.fields['quantity'].required = True
        self.fields['expiration_date'].required = True

class RegisterForm(forms.ModelForm):
    # password_confirm = forms.PasswordInput()

    class Meta():
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_active']
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez le nom utilisateur',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez le prénom',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez le nom',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez l’adresse e-mail',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le mot de passe',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            # 'password_confirm': forms.PasswordInput(attrs={
            #     'class': 'form-control',
            #     # 'placeholder': 'Entrez à nouveau le mot de passe',
            #     'placeholder': '&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;&#xb7;',
            #     'required': True,
            # }),
        }

        labels = {
            'username': 'Nom utilisateur',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Adresse e-mail',
            'password': 'Mot de passe',
            'is_active': 'Est actif',
            # 'password_confirm': 'Confirmer mot de passe',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir les champs requis
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = False
        self.fields['email'].required = True
        self.fields['password'].required = False
        
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Ce nom d’utilisateur est déjà pris.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("L'adresse email est déjà pris.")
        return email
    
class LoginForm(forms.ModelForm):
    credential = forms.CharField()
    password = forms.CharField()
    
    class Meta():
        model = User
        fields = ['credential', 'password']
        widgets = {
            'credential': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email ou Nom utilisateur',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mot de passe',
            }),
        }
        
        labels = {
            'credential': 'Email ou Nom utilisateur',
            'password': 'Mot de passe',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir les champs requis
        self.fields['credential'].required = True
        self.fields['password'].required = True

class EmployeeForm(forms.ModelForm):
    class Meta():
        model = Employee
        # exclude = ('user',)
        # agree_privacy_policy
        # 'employee_pic',
        fields = [ 'position', 'salary_brut', 'phone_number', 'roles' ]
        
        widgets = {
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Saisir l\'Intintulé du Poste Occupé',
            }),
            'salary_brut': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Entrez le Salaire brut',
            }),
            'roles': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'empty_label': 'Sélectionnez les roles',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Saisir la biography',
            }),
            # 'country': forms.Select(attrs={
            #     'class': 'form-control',
            #     'empty_label': 'Sélectionnez son pays d\'action',
            # }),
            # 'birth_date': forms.DateInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Choisir date de naissance',
            #     'type': 'date'
            # }),
            # 'biography': forms.Textarea(attrs={
            #     'class': 'form-control',
            #     # 'cols': 20,
            #     'rows': 2,
            #     'placeholder': 'Entrez la biographie ici...',
            # }),
            
            # 'agree_privacy_policy': forms.CheckboxInput(attrs={
            #     'class': 'form-check-input'
            # }),
            # 'employee_pic': forms.ClearableFileInput(attrs={
            #     'class': 'form-control',
            #     'accept': 'image/*',
            # }),
        }
        
        labels = {
            'salary_brut': 'Salaire de base de l\'employé',
            'position': 'Intintulé du Poste Occupé',
            'roles': 'Roles d\'accès',
            'phone_number': 'Numero de téléphone',
            # 'country': 'Sélectionnez le pays d\'activité',
            # 'location': 'Saisir sa localité',
            # 'biography': 'Biographie',
            # 'agree_privacy_policy': 'J\'accepte la politique d\'accord',
            # 'birth_date': 'Date de naissance',
            # 'employee_pic': 'Image de l\'utilisateur',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir les champs requis
        self.fields['salary_brut'].required = False
        self.fields['position'].required = False
        self.fields['roles'].required = True
        self.fields['phone_number'].required = False
        # self.fields['country'].required = True
        # self.fields['location'].required = False
        # self.fields['biography'].required = False
        # self.fields['agree_privacy_policy'].required = False
        # self.fields['birth_date'].required = False

class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('user', 'loyalty_point', 'updated_by', 'created_at', 'updated_at', )
        # fields = [ 'first_name', 'last_name', 'email', 'phone_number', 'phone_number_other', 'address', 'country', 'city']

        # Custom widgets and attributes for each field
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez le prénom',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez le nom',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez l’adresse e-mail',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez le numéro de téléphone',
            }),
            'phone_number_other': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez un autre numéro de téléphone (optionnel)',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez l’adresse (optionnel)',
                'rows': 2,
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez le pays (optionnel)',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez la ville (optionnel)',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrez le nom de l’entreprise (optionnel)',
            }),
            # 'loyalty_point': forms.NumberInput(attrs={
            #     'class': 'form-control mb-3',
            #     'placeholder': 'Points de fidélité',
            #     'required': True,
            #     'min': 0,
            # }),
        }

        # Optional: Custom labels for fields
        labels = {
            'first_name': 'Prénom du client',
            'last_name': 'Nom du client',
            'email': 'Adresse e-mail du client',
            'phone_number': 'Numéro de téléphone du client',
            'phone_number_other': 'Autre numéro de téléphone du client',
            'address': 'Adresse du client',
            'country': 'Pays du client',
            'city': 'Ville du client',
            'company': 'Entreprise du client',
            # 'loyalty_point': 'Points de fidélité',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Définir les champs requis
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True
        self.fields['phone_number_other'].required = False
        self.fields['address'].required = True
        self.fields['country'].required = True
        self.fields['city'].required = True
        self.fields['company'].required = False
                
        
    # # Additional validations can be added here if necessary
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     # Custom validation for email, if needed
    #     if not email.endswith('.com'):
    #         raise forms.ValidationError("L'adresse e-mail doit se terminer par '.com'.")
    #     return email
        
class PayrollFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True)

# class SaleForm(forms.ModelForm):
#     class Meta:
#         model = Sale
#         fields = ['user', 'client', 'discount', 'ht_amount', 'sale_date', 'country']

#     def __init__(self, *args, **kwargs):
#         """
#         Add placeholders and classes, remove auto-generated
#         labels and set autofocus on first field
#         """
#         super().__init__(*args, **kwargs)
#         placeholders = {
#             'full_name': 'Full Name',
#             'email': 'Email Address',
#             'phone_number': 'Phone Number',
#             'postcode': 'Postal Code',
#             'city': 'City',
#             'street_address1': 'Street Address 1',
#             'street_address2': 'Street Address 2',
#             'country': 'country, State or Locality',
#         }

#         self.fields['full_name'].widget.attrs['autofocus'] = True
#         for field in self.fields:
#             if field != 'country':
#                 if self.fields[field].required:
#                     placeholder = f'{placeholders[field]} *'
#                 else:
#                     placeholder = placeholders[field]
#                 self.fields[field].widget.attrs['placeholder'] = placeholder
#             self.fields[field].widget.attrs['class'] = 'stripe-style-input'
#             self.fields[field].label = False


