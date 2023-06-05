from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm 

# function based
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token 
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, get_user_model

# Create your views here.

class SignupView(CreateView):
    form_class = CustomUserCreationForm 
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


def usersignup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False) 
            user.is_active = False 
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate your account'
            message = render_to_string('registration/activate_account.html', {
                'user': user, 
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have send you an email, please confirm your email address to complete registration')
    else:
            form  = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True 
        user.save()    

    return redirect('login')


