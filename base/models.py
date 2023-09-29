from django.db import models
from accounts.models import CustomUser
# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 

class Book(models.Model):
    title = models.CharField(max_length=255) 
    authors = models.ManyToManyField(Author) 
    genres = models.ManyToManyField(Genre) 
    description = models.TextField() 
    publication_date = models.DateField() 
    cover_image = models.ImageField(upload_to='book_cover/')
    total_page = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    def average_rating(self):
        # Calculate and return the average rating for the book
        ratings = self.ratings.all()
        if ratings:
            return sum(rating.value for rating in ratings) / len(ratings)
        else:
            return 0 
    
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE) 
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review_text[0: 50]
    

class ReadingStatus(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    progress = models.PositiveIntegerField(default = 0)


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    reading_books = models.ManyToManyField(ReadingStatus, related_name='reading_users')
    to_read_books = models.ManyToManyField(ReadingStatus, related_name='to_read_users')
    finished_books = models.ManyToManyField(ReadingStatus, related_name='finished_users')


class Rating(models.Model):
    book = models.ForeignKey(Book, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ('book', 'user')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.save()  # Save the book to trigger the average_rating update

    def __str__(self):
        return self.book.title 