from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.conf import settings

from . import views
from .forms import UserAuthenticatorForm

urlpatterns = [
    path("login/", LoginView.as_view(template_name="accounts/login.html", redirect_authenticated_user=True, form_class=UserAuthenticatorForm), name='login'),
    path("logout/", LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("", views.profile, name="profile"),
    path("edit/", views.edit_profile, name="edit_profile"),

    path('password-reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
