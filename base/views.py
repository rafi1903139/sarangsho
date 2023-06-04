from django.shortcuts import render, redirect
from .models import Genre, Book
from django.db.models import Q 
from accounts.models import CustomUser
# Create your views here.

def userProfile(request, pk):
    user = CustomUser.objects.get(id = pk)
    context = {'user': user}

    return render(request, 'base/user_profile.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if q != '':
        books = Book.objects.filter(
            Q(title__icontains=q)
        )
        genres = {'title': 'Search found'}
        context = {'genres': genres, 'books': books}
        return render(request, 'base/book_list.html', context) 
        
    genres = Genre.objects.all()
    books = Book.objects.all()
    context = {'genres': genres, 'books': books}
    return render(request, 'base/home.html', context)


def book_details(request, pk):
    book = Book.objects.get(id=pk)
    authors = book.authors.all()
    context = {'book': book, 'authors': authors}

    return render(request, 'base/book_detail.html', context)

def book_list(request, pk):
    genre = Genre.objects.get(id=pk)
    books = genre.book_set.all()
    context = {'genre': genre, 'books': books}

    return render(request, 'base/book_list.html', context)