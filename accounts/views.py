from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model

from Wardrobe import settings
from .forms import UserRegistrationForm, UserUpdateForm, UserPasswordChangeForm
from orders.models import Order
from .tokens import account_activation_token


def signup(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False

            # send email
            mail_subject = 'Activate your Wardrobe user account'
            message = render_to_string('accounts/activate_email.html', {
                'first_name': user.first_name,
                'domain': get_current_site(request).domain,
                'email': urlsafe_base64_encode(force_bytes(user.email)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(mail_subject, message, to=[user.email])

            # we save the account only if the email is sent, otherwise we tell the user to try later
            if email.send():
                user.save()
                return render(request, 'accounts/activate_sent.html', {'email': user.email})
            else:
                form.add_error(None, "Impossibile inviare l'email di attivazione account. Provare a registrarsi più tardi")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/signup.html', {'form': form})


def activate(request, emailb64, token):
    User = get_user_model()
    try:
        email = force_str(urlsafe_base64_decode(emailb64))
        myuser = User.objects.get(email=email)
    except (TypeError,ValueError,OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and account_activation_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        return render(request, 'accounts/activate_success.html')
    else:
        return render(request,'accounts/activate_failed.html')


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user.id).prefetch_related('orderitem_set')
    return render(request, 'accounts/profile.html', {'orders': orders})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)  # Passa l'istanza dell'utente
        if form.is_valid():
            form.save()  # Salva i dati del modulo
            login(request, request.user)
            return redirect('profile')  # Reindirizza all'URL 'profile' (assicurati di avere questo URL configurato)
    else:
        form = UserUpdateForm(instance=request.user)  # Precompila il modulo con i dati dell'utente

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)  # Passa l'istanza dell'utente
        if form.is_valid():
            form.save()  # Salva i dati del modulo
            login(request, request.user)
            return redirect('profile')  # Reindirizza all'URL 'profile' (assicurati di avere questo URL configurato)
    else:
        form = UserPasswordChangeForm(request.user)  # Precompila il modulo con i dati dell'utente

    return render(request, 'accounts/change_password.html', {'form': form})
