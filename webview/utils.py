# from django.conf import settings
from decimal import Decimal, InvalidOperation
import os
from django.core.paginator import Paginator

from .templatetags.functions_extras import to_int
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import datetime

def createAppSite(id=1):
    from django.contrib.sites.models import Site
    from webview.models import AppSite
    try:
        # Retrieve or create the Site instance
        try:
            site = Site.objects.get(id=id)
        except Site.DoesNotExist:
            site = Site(id=id)

        # Set Site fields
        site.name = AppSite.NAME
        site.domain = AppSite.DOMAIN
        site.save()

        # Retrieve or create the AppSite instance
        try:
            app_site = AppSite.objects.get(site=site)
        except Exception:
            app_site = AppSite(site=site)

        # Set AppSite fields correctly (no commas at the end)
        app_site.id = site.id
        app_site.email = AppSite.EMAIL
        app_site.phone_number = AppSite.PHONE1
        app_site.phone_number_other = AppSite.PHONE2
        app_site.address = AppSite.ADDRESS
        app_site.save()

        return True
    except Exception:
        return False


def notEmpty(data)->bool:
    return data and data is not None and data != '' and data != ' ' and data != 'None' and data != [] and data != '[]' and data != {} and data != '{}'

def Pagination(request, data, num = 10):
        paginator = Paginator(data, num)
        page = request.GET.get('page')
        try:
            paginate = paginator.page(to_int(page))
            return paginate
        except Exception:
            paginate = paginator.page(1)
            return paginate
   
def send_sale_notification(client, sale):
    subject = 'Nouvelle facture créée'
    html_message = render_to_string('sales/email_sale.html', {'client': client, 'sale': sale})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = client.email
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def getTax(employee, totalHT):
    """ Return 'tax_rate_brut', 'tax_rate', 'tax_amount' """
    taxRateBrut = (float(employee.country.tax) if employee.country and employee.country.tax is not None and employee.country.tax > 0 else 0.0)
    taxRate = (taxRateBrut / 100) if taxRateBrut > 1 else taxRateBrut
    taxAmount = (float(totalHT) * taxRate)
    return {'tax_rate_brut': taxRateBrut, 'tax_rate': taxRate, 'tax_amount': taxAmount }

def get_TTC_amount(employee, totalHT, discount, applyTax = True):
    discount = float(discount) if discount else 0.0
    gTax = getTax(employee, totalHT)
    tax = gTax.tax_amount if applyTax else 0
    totalTTC = float(totalHT) + tax - discount
    return totalTTC

def safeDecimal(value, tryNull=False):
    try:
        # Replace comma with period for decimal conversion
        value = value.replace(',', '.')
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return Decimal('0') if not tryNull else None
    
def safeFloat(value):
    try:
        # Replace comma with period for float conversion
        value = value.replace(',', '.')
        return float(value)
    except ValueError:
        return 0.0



def parseDatetime(date_str):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

def parseDate(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')


def paymentStatusList() -> list[dict[str, str]]:
    return [
        {'id': 'paid', 'name': 'Payée'},
        {'id': 'pending', 'name': 'En cours'},
        {'id': 'overdue', 'name': 'En retard'}
    ]



def read_base64_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()
    
def save_pdf_file(output_path, pdf):
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    with open(output_path, 'wb') as f:
        f.write(pdf)
        
        

def get_years_list(start_year: int = 2022) -> list[int]:
    current_year = get_current_year()
    
    if start_year == current_year:
        return [current_year]
    
    if start_year < current_year:
        years = [current_year - i for i in range(current_year - start_year + 1)]
        return sorted(years)
    
    return [start_year]

def get_current_year(date: str = None) -> int:
    try:
        formatted_date = format_date(datetime.fromisoformat(date)) if date else format_date(datetime.now())
        return int(formatted_date)
    except Exception:
        return int(format_date(datetime.now()))

def format_date(date: datetime) -> str:
    return str(date.year)
  
        
        
        
        