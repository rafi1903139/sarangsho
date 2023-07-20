from django.shortcuts import render, redirect
from .models import Genre, Book, Review, ReadingStatus, UserProfile
from django.db.models import Q 
from accounts.models import CustomUser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json 



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

    # get the activity of the users that the current user is following
    print(request.user)
    following_users = request.user.following.all() if request.user.id != None else []
    
    activity = []
    
 
    for f_user in following_users:
        activity += Review.objects.filter(user=f_user)
            
    
    
    
    
    context = {'genres': genres, 'books': books, 'activities': activity}
    return render(request, 'base/home.html', context)


def book_details(request, pk):
    book = Book.objects.get(id=pk)
    authors = book.authors.all()
    reviews = Review.objects.filter(book__id__contains=book.id)

    try:
        user_status = ReadingStatus.objects.get(book=book, user=request.user);
    except ObjectDoesNotExist:
        user_status = None
    
    
    followers = request.user.following.all() if request.user.id != None else []
 
    context = {'book': book, 'authors': authors, 'reviews': reviews, 'followers': followers, 'user_status': user_status}

    return render(request, 'base/book_detail.html', context)

def book_list(request, pk):
    genre = Genre.objects.get(id=pk)
    books = genre.book_set.all()
    context = {'genre': genre, 'books': books}

    return render(request, 'base/book_list.html', context)

def book_review(request, pk):

    if request.method == 'POST':
            

        Review.objects.create(
            user = request.user,
            book = Book.objects.get(id=pk),
            review_text = request.POST.get('review')
        )
        
        return redirect('book_detail', pk)
    
    return render(request, 'base/review_form.html', {})


@csrf_exempt
def follow_view(request):
    user_id = request.POST.get("user_id")

        
    user = CustomUser.objects.get(id=user_id)
    followers = user.followers.all()


    if request.user in followers:
        # already following then unfollow
        print('unfollow user')
        user.followers.remove(request.user)
    else:
        # add the user as a follower
        print('follow user')
        user.followers.add(request.user)

    return HttpResponse(status=200)

def add_to_read(request, user_id, book_id):
    
    if request.method == 'POST':
        # add book to the user shelf
        user_status = json.loads(request.body);
        print(user_status['status'])

    try:
        user_reading_status = ReadingStatus.objects.get(book=Book.objects.get(id=book_id), user=request.user);
        user_reading_status.status = user_status['status']
        user_reading_status.save()
    
    except ObjectDoesNotExist:
        # create Reading status object for the user if not exist
        status_id = ReadingStatus.objects.create(
            user = CustomUser.objects.get(id=user_id),
            book = Book.objects.get(id=book_id),
            status = user_status['status']
        )
        print(status_id)
        return HttpResponse(status=200)
    
    return HttpResponse(status=200)
    