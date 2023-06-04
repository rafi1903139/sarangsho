from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/<str:pk>/", views.book_details, name="book_detail"),
    path("genre/<str:pk>/", views.book_list, name="book_list"),
    path("profile/<str:pk>/", views.userProfile, name="user_profile"),
]
