from django.db import models
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

    def __str__(self):
        return self.title 
