import os
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from django.conf import settings

from webview.utils import notEmpty
from .tokens import account_activation_token
import logging


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Set up logging
logger = logging.getLogger(__name__)


def send_email_with_attachment(recipient_email, subject , body, attachment_path):
    
    smtp_server = settings.EMAIL_HOST 
    smtp_port = settings.EMAIL_PORT 
    sender_email = settings.DEFAULT_FROM_EMAIL 
    sender_password = settings.EMAIL_HOST_PASSWORD
     
    # Create message container
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Attach email body
    body_part = MIMEText(body, 'plain')
    msg.attach(body_part)

        # Attach the PDF file
    with open(attachment_path, 'rb') as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)


    # Send the email using SMTP
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f'Email sent to {recipient_email}')
    except Exception as e:
        print(f'Failed to send email: {str(e)}')


def send_activation_email(request, user)-> bool:
    try:
        # Get the current site details
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        
        # Render HTML content from your email template
        html_message = render_to_string('accounts/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'base_url': settings.BASE_URL,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        
        # Strip HTML tags to create a plain text version for email clients that don't support HTML
        plain_message = strip_tags(html_message)
        
        # Define email parameters
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.email]
        
        # Create the email message object
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=from_email,
            to=to_email,
        )
        
        # Attach the HTML version as an alternative
        email.attach_alternative(html_message, "text/html")
        
        # Send the email
        email.send(fail_silently=False)
        logger.info(f"Activation email sent to {user.email}")
        return True

    except Exception as e:
        # Log the exception with stack trace for better debugging
        logger.error(f"Error sending activation email to {user.email}: {e}", exc_info=True)
        return False


# def images_dir(file=""):
#     if file != "":
#         return os.path.join(os.path.abspath(os.path.dirname('media/images/')), file)
#     else:
#         return os.path.abspath(os.path.dirname('media/images/'))

def users_pictures_path(instance, filename):
    from os.path import basename
    basename(filename)
    filename, fileExtension = os.path.splitext(filename)
    
    try:
        user_id = instance.user.id if instance and instance.user and notEmpty(instance.user.id) else 1
    except Exception:
        user_id = 1
    
    return f'employees_pictures/{user_id}/{hash(filename)}{fileExtension}'


def users_pictures_path_thumb(instance, filename):
    from os.path import basename
    basename(filename)
    filename, fileExtension = os.path.splitext(filename)
    
    try:
        user_id = instance.user.id if instance and instance.user and notEmpty(instance.user.id) else 1
    except Exception:
        user_id = 1
    return f'employees_pictures/{user_id}/thumb/{hash(filename)}-thumb{fileExtension}'


def products_pictures_path(instance, filename):
    from os.path import basename
    basename(filename)
    filename, fileExtension = os.path.splitext(filename)
    
    try:
        user_id = instance.user.id if instance and instance.user and notEmpty(instance.user.id) else 1
    except Exception:
        user_id = 1
    return f'products_pictures/{user_id}-{hash(filename)}{fileExtension}'


def products_pictures_path_thumb(instance, filename):
    from os.path import basename
    basename(filename)
    filename, fileExtension = os.path.splitext(filename)
    
    try:
        user_id = instance.user.id if instance and instance.user and notEmpty(instance.user.id) else 1
    except Exception:
        user_id = 1
    return f'products_pictures/thumb/{user_id}-{hash(filename)}-thumb{fileExtension}'


# def send_activation_email(request, user):
#     from django.utils.http import urlsafe_base64_encode
#     from django.utils.encoding import force_bytes
#     from django.template.loader import render_to_string
#     from django.core.mail import send_mail
#     from django.contrib.sites.shortcuts import get_current_site
#     from django.utils.html import strip_tags
#     from django.conf import settings
#     from .tokens import account_activation_token

#     try:
#         current_site = get_current_site(request)
#         subject = 'Activate Your Account'

#         # Render HTML content from your template
#         html_message = render_to_string('accounts/account_activation_email.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': account_activation_token.make_token(user),
#         })
        
#         # Strip HTML tags to create a plain text version
#         plain_message = strip_tags(html_message)

#         # Send the email with both plain text and HTML content
#         send_mail(
#             subject,
#             plain_message,  # Plain text version
#             settings.DEFAULT_FROM_EMAIL,
#             [user.email],
#             html_message=html_message  # HTML content
#         )

#         return True
#     except Exception as e:
#         print(f'Error sending activation email: {e}')
#         return False
# def send_test_email():
#     import smtplib
#     from email.mime.text import MIMEText
#     from django.conf import settings
#     from django.http import HttpResponse
#     # EMAIL_USE_TLS
#     try:
#         email_user = settings.DEFAULT_FROM_EMAIL
#         with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10) as server:
#             server.starttls()
#             server.login(email_user, settings.EMAIL_HOST_PASSWORD)

#             msg = MIMEText("This is a test email.")
#             msg["Subject"] = "Test Subject"
#             msg["From"] = email_user
#             msg["To"] = "kossi.tsolegnagbo@gmail.com"

#             server.sendmail(msg["From"], msg["To"], msg.as_string())
#         return HttpResponse("Email sent successfully!")
#     except smtplib.SMTPException as e:
#         return HttpResponse(f"An SMTP error occurred: {e}", status=500)
#     except Exception as e:
#         return HttpResponse(f"An error occurred: {e}", status=500)

# def send_test_email2(request):
#     import smtplib
#     from email.mime.text import MIMEText
#     from django.shortcuts import HttpResponse
#     # from django.core.mail import send_mail
#     # from django.conf.urls.static import static
#     from django.conf import settings
#     from django.core.mail import EmailMessage
#     from django.template.loader import render_to_string
#     from django.contrib.sites.shortcuts import get_current_site
    
#     email_user = settings.DEFAULT_FROM_EMAIL
#     subject = "Test Subject"
    
#     current_site = get_current_site(request)
    
#     # Render HTML content
#     html_content = render_to_string('accounts/account_activation_email.html', {
#                                 'user': 'user',
#                                 'domain': current_site.domain,
#                                 'uid': 'urlsafe_base64_encode(force_bytes(user.pk))',
#                                 'token': 'account_activation_token.make_token(user)',
#                             })
    
#     try:
#         email = EmailMessage(
#             subject,
#             html_content,
#             email_user,
#             ['kossi.tsolegnagbo@gmail.com']
#         )
#         email.content_subtype = "html"  # Main content is now text/html
#         email.send()
#         print('Email sent successfully!')
#     except Exception as e:
#         print(f'Error sending email: {e}')
        
        
        
        