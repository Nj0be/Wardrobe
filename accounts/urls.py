from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings

from . import views
from .forms import UserAuthenticatorForm

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html", redirect_authenticated_user=True, form_class=UserAuthenticatorForm), name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]
