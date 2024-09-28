import hashlib
from django import template

from django.contrib import messages

register = template.Library()


@register.filter(is_safe=True, name="get_items")
def get_items(value, arg):
    """get_items."""
    data = value[0]
    return data.items()

    
@register.filter(is_safe=True, name="substract")
def substract(x,y):
    return x - y

@register.filter(is_safe=True, name="aggragate_sum")
def aggragate_sum(value1, value2):
    """show month label."""
    if value1 is not None and value1 != "" and value2 is not None and value2 != "":
        d = to_int(value1) + to_int(value2)
        return d
    return ""


@register.filter(is_safe=True, name="to_int")
def to_int(value):
    """Convert to integer."""
    if value is None or value == "":
        return 0
    return int(float(value))


@register.filter(is_safe=True, name="separate_millier")
def separate_millier(n, sep=" "):
    """separate data with arg"""
    if n is None or n == "":
        return 0
    s = str(n)
    ll = len(s)
    d = ll/3
    for i in range(1, to_int(d)+1):
        s = s[:ll-3*i] + sep + s[ll-3*i:]
    return s

@register.filter(is_safe=True, name="url_matched")
def url_matched(url, arg=""):
    """Return True if split url matched arg"""
    try:
        page1 = url.split('/')[2]
        try:
            page2 = url.split('/')[3]
        except Exception:
            page2 = ""
        if arg != "":
            if page1 == arg or page2 == arg and page2 != "":
                return True 
            else:
                return False
        else:
            if page2 != "":
                return page2
            else:
                return page1
    except Exception:
        return False


@register.filter(is_safe=True, name="trans")
def trans(value, request):
    """translate params given into english or french"""
    return value

def UserIsConnect(request):
    if request.user.is_authenticated:
        # messages.info(request, trans("Vous Êtes Déja Connecté!", request))
        return True
    else:
        if request.GET.get('next') is not None and request.GET.get('next') != "":
            messages.error(request, trans("Authentifier Vous Pour Accéder A La Page Demandée!", request))
        else:
            pass
        return False

def sha1Hash(value1, value2='', value3=''):
    """algorithm = sha1"""
    if value2 == '' and value3 == '':
        hash = hashlib.sha1((str(value1)).encode()).hexdigest()
    else:
        hash = hashlib.sha1((str(value1) + str(value2) + str(value3)).encode()).hexdigest()
    return hash

def sha256Hash(value1, value2='', value3=''):
    """algorithm = sha256"""
    if value2 == '' and value3 == '':
        hash = hashlib.sha256((str(value1)).encode()).hexdigest()
    else:
        hash = hashlib.sha256((str(value1) + str(value2) + str(value3)).encode()).hexdigest()
    return hash

def MD5Hash(value1, value2='', value3=''):
    """algorithm = md5"""
    if value2 == '' and value3 == '':
        hash = hashlib.md5((str(value1)).encode()).hexdigest()
    else:
        hash = hashlib.md5((str(value1) + str(value2) + str(value3)).encode()).hexdigest()
    return hash


def SuccessSaveMessage(request):
    return trans("Sauvegardé avec Succès!", request)

def SuccessUpdateMessage(request):
    return trans("Modifié avec Succès!", request)

def SuccessDeleteMessage(request):
    return trans("Supprimé avec Succès!", request)

def IntegrityErrorMessage(request):
    return trans("Action Impossible, Elément utilisé dans d'autres pages", request)

def SaisieErrorMessage(request):
    return trans("Erreur de Saisie! Veuillez Revérifier SVP !!!", request)

def PageNotFoundMessage(request):
    return trans("La Page demandée n'est pas disponible pour le moment", request)

def DateErrorMessage(request):
    return trans("Renseigné correctement les dates !", request)

def YearErrorMessage(request):
    return trans("Renseigné correctement l'année !", request)

def RequestHaveErrorMessage(request):
    return trans("La Requete demandée comporte des erreurs !", request)

def LanguageChangedMessage(request):
    return trans("Langue Changée", request)

def ParameterErrorMessage(request):
    return trans("Paramettre Non Pris En Charge !", request)

def LoggedInSuccessMessage(request):
    return trans("Vous vous êtes connecté avec Succès!", request)

def InactiveAccountMessage(request):
    return trans("Votre Compte est inactif! contacter votre administrateur SVP.", request)

def IncorectLoginInfosMessage(request):
    return trans("informations d'identification incorrectes. Réessayer!", request)

def RequireAuthenticateMessage(request):
    return trans("Authentification Requise", request)

def LogoutSuccessMessage(request):
    return trans("Vous Êtes Déconnecté!", request)
