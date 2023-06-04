from django import forms 
from .models import CustomUser 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="Required")
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'description')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'description')
        