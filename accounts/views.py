from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .forms import UserRegistrationForm, UserUpdateForm
from orders.models import Order


def signup(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("homepage")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/signup.html', {'form': form})


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
