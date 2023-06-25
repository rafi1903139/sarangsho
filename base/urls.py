from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books/<str:pk>/", views.book_details, name="book_detail"),
    path("genre/<str:pk>/", views.book_list, name="book_list"),
    path("profile/<str:pk>/", views.userProfile, name="user_profile"),
    path("review/new/<str:pk>", views.book_review, name="book_review"),
    path("follow/", views.follow_view, name='follow')
]
