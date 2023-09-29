from django.shortcuts import render, redirect
from .models import Genre, Book, Review, ReadingStatus, UserProfile, Rating
from django.db.models import Q
from accounts.models import CustomUser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json


# Create your views here.


def userProfile(request, pk):
    if request.user.id == None:
        return redirect('home')
    
    user = CustomUser.objects.get(id=pk)
    bookshelve = ReadingStatus.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    currently_reading = []
    read = []
    want_to_read = []

    for item in bookshelve:
        if item.status == "Want to read":
            want_to_read.append(item.book)
        elif item.status == "Currently Reading":
            currently_reading.append(item.book)
        elif item.status == "Read":
            read.append(item.book)

    books = {
        "currently_reading": currently_reading,
        "want_to_read": want_to_read,
        "read": read,
    }
    context = {"user": user, "books": books, "reviews": reviews}

    return render(request, "base/user_profile.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    if q != "":
        books = Book.objects.filter(Q(title__icontains=q))
        genres = {"title": "Search found"}
        isListByCategory = False

        context = {
            "genres": genres,
            "books": books,
            "isListByCategory": isListByCategory,
        }
        return render(request, "base/book_list.html", context)

    genres = Genre.objects.all()
    books = Book.objects.all()

    # get the activity of the users that the current user is following
    print(request.user)

    # get the update of user reading status
    current_reading_status = get_user_reading_status(request)

    # get currentyle readiing books
    current_reading_book = None
    if request.user.id != None:
        items = ReadingStatus.objects.filter(
            user=request.user, status="Currently Reading"
        )
        for item in items:
            current_reading_book = item.book

    following_users = request.user.following.all() if request.user.id != None else []

    activity = []

    for f_user in following_users:
        activity += Review.objects.filter(user=f_user)

    context = {
        "genres": genres,
        "books": books,
        "activities": activity,
        "current_reading_book": current_reading_book,
        "current_reading_status": current_reading_status,
    }
    return render(request, "base/home.html", context)


def book_details(request, pk):
    book = Book.objects.get(id=pk)
    authors = book.authors.all()
    reviews = Review.objects.filter(book__id__contains=book.id)

    for review in reviews:
        review.rating = 0
        ratings = Rating.objects.filter(user=review.user, book=book)
        if ratings:
            for rating in ratings:
                review.rating = rating.value

        print(review.rating)

    # get the user reading status and followers
    user_status = None
    followers = []

    if request.user.id != None:
        try:
            user_status = ReadingStatus.objects.get(book=book, user=request.user)
        except ObjectDoesNotExist:
            print('status is not provided')
    
    followers = request.user.following.all()

    context = {
        "book": book,
        "authors": authors,
        "reviews": reviews,
        "followers": followers,
        "user_status": user_status,
    }

    return render(request, "base/book_detail.html", context)


def book_list(request, pk):
    genre = Genre.objects.get(id=pk)
    books = genre.book_set.all()
    isListByCategory = True

    context = {"genre": genre, "books": books, "isListByCategory": isListByCategory}

    return render(request, "base/book_list.html", context)


def book_review(request, pk):
    if request.user.id == None:
        return redirect('home')
    
    

    if request.method == "POST":
        book=Book.objects.get(id=pk)
        reviews = Review.objects.filter(user=request.user, book=book)
        
        for review in reviews:
            Review.delete(review)

        Review.objects.create(
            user=request.user,
            book=book,
            review_text=request.POST.get("review"),
        )

        return redirect("book_detail", pk)

    return render(request, "base/review_form.html", {})


@csrf_exempt
def follow_view(request):
    user_id = request.POST.get("user_id")

    user = CustomUser.objects.get(id=user_id)
    followers = user.followers.all()

    if request.user in followers:
        # already following then unfollow
        print("unfollow user")
        user.followers.remove(request.user)
    else:
        # add the user as a follower
        print("follow user")
        user.followers.add(request.user)

    return HttpResponse(status=200)


def add_to_read(request, user_id, book_id):
    if request.method == "POST":
        # add book to the user shelf
        user_status = json.loads(request.body)
        print(user_status["status"])

    try:
        user_reading_status = ReadingStatus.objects.get(
            book=Book.objects.get(id=book_id), user=request.user
        )
        if user_status["status"] == "Remove":
            ReadingStatus.delete(
                ReadingStatus.objects.get(
                    book=Book.objects.get(id=book_id), user=request.user
                )
            )
            print("Successfully removed")
        else:
            user_reading_status.status = user_status["status"]
            user_reading_status.save()
            print("Successfully updated reading status")

    except ObjectDoesNotExist:
        # create Reading status object for the user if not exist
        status_id = ReadingStatus.objects.create(
            user=CustomUser.objects.get(id=user_id),
            book=Book.objects.get(id=book_id),
            status=user_status["status"],
        )

    return HttpResponse(status=200)


@csrf_exempt
def add_rating(request, book_id, user_id):
    if request.method == "POST":
        user_rating = json.loads(request.body)
        ratings = Rating.objects.filter(book=Book.objects.get(id=book_id), user=request.user)
        
        for rating in ratings:
            Rating.delete(rating)

        Rating.objects.create(
            book=Book.objects.get(id=book_id),
            user=CustomUser.objects.get(id=user_id),
            value=user_rating["rating"],
        )

        response = {"status": "success", "message": "Successfully added rating"}

        return JsonResponse(response)


def get_user_reading_status(request):
    if not request.user.is_anonymous:
        # get the bookshelf of the user
        # book name - Reading status

        bookshelve = ReadingStatus.objects.filter(user=request.user)

        already_read_count = 0
        currently_reading_count = 0
        want_to_read_count = 0

        for status in bookshelve:
            if status.status == "Want to read":
                want_to_read_count = want_to_read_count + 1
            elif status.status == "Currently Reading":
                currently_reading_count = currently_reading_count + 1
            elif status.status == "Read":
                already_read_count = already_read_count + 1

        current_reading_status = {
            "wr": want_to_read_count,
            "cr": currently_reading_count,
            "ar": already_read_count,
        }
        return current_reading_status

    else:
        return {}
