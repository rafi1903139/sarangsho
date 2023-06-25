from django.urls import path 
from . import views 

urlpatterns = [
    path('signup/', views.usersignup, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

]