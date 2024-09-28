from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def error403(request, exception=None):
    return render(request, 'errors/404.html', {'error_code': 403}) 

def error404(request, exception=None):
    return render(request, 'errors/404.html', {'error_code': 404})

def error500(request, exception=None):
    return render(request, 'errors/500.html') 

@csrf_exempt
def csrf_failure(request, reason="csrf error"):
    return render(request, 'errors/csrf_error.html')
