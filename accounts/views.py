from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm 
from .models import CustomUser

# function based
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token 
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

# Create your views here.

def loginPage(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('home') 
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")
            return render(request, "accounts/login_register.html", context)
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "accounts/login_register.html", context)
    
    return render(request, "accounts/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect('home')




class SignupView(CreateView):
    form_class = CustomUserCreationForm 
    success_url = reverse_lazy('login')
    template_name = "accounts/login_register.html"


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
    return render(request, 'accounts/login_register.html', {'form': form})

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


