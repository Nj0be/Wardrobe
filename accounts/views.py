from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .forms import UserRegisterForm, UserUpdateForm
from orders.models import Order


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


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user.id).prefetch_related('orderproduct_set')
    return render(request, 'accounts/profile.html', {'orders': orders})


@login_required
def edit_profile(request):
    user = request.user  # Ottieni l'utente attualmente autenticato

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)  # Passa l'istanza dell'utente
        if form.is_valid():
            form.save()  # Salva i dati del modulo
            login(request, user) # Esegui il login dell'utente
            return redirect('profile')  # Reindirizza all'URL 'profile' (assicurati di avere questo URL configurato)
    else:
        form = UserUpdateForm(instance=user)  # Precompila il modulo con i dati dell'utente

    return render(request, 'accounts/edit_profile.html', {'form': form})

