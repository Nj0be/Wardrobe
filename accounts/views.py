from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import UserRegisterForm


class SignupView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # L'utente è già loggato, lo reindirizziamo alla homepage
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)
