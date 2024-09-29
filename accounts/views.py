from django.http import HttpResponse
from django.contrib.auth import views as auth_views

class LoginView(auth_views.LoginView):
    template_name = "accounts:login.html"
    next_page = "products:homepage"
    # authentication_form: A callable (typically a form class) to use for authentication. Defaults to AuthenticationForm.
    redirect_authenticated_user = True # C'è un warning sul metterlo true, visita: https://docs.djangoproject.com/en/5.1/topics/auth/default/#django.contrib.auth.views.LoginView per saperne di più

def signup(request):
    return HttpResponse("Hello, world. You're at the signup page.")
