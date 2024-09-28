# signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from webview.utils import createAppSite
from .models import AppSite, Country, Role

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    """
    Create default roles if none exist in the database.
    This runs after each migration.
    """
    # List of default roles
    default_roles = [
        {'id':'admin', 'name':'Administrateur Global'},
        {'id':'user_payroll', 'name':'Peut payer de salaire'},
        {'id':'dashboard', 'name':'Peut voir Tableaux de bord'},
        {'id':'user', 'name':'Simple utilisateur'},
        # {'id':'secretary', 'name':'Secrétaire'},
        # {'id':'sales_agent', 'name':'Agent commercial'},
    ]

    default_countries = [
        {'name': 'Togo', 'tax': 18.00},
        {'name': 'Bénin', 'tax': 18.00},
        {'name': 'Burkina Fasso', 'tax': 18.00},  # Assuming a default tax value for Burkina Fasso
    ]

    # Check if any roles exist; if not, create the defaults
    # if Role.objects.count() == 0:
    if not Role.objects.exists():
        for role in default_roles:
            Role.objects.get_or_create(id=role['id'], name=role['name'])
        print("Default roles have been created.")
    
    
    # Check if no countries exist, and create the defaults
    if not Country.objects.exists():  # More efficient than using count()
        for country_data in default_countries:
            Country.objects.get_or_create(
                name=country_data['name'],
                defaults={'tax': country_data['tax']}
            )
        print("Default countries have been created.")
    
    
    # Check if no countries exist, and create the defaults
    if not AppSite.objects.exists():  # More efficient than using count()
        createAppSite(id=1)
        print("Default AppSite have been created.")
        
        

    
