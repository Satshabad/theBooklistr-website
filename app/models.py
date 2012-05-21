from django.db import models

# Create your models here# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=30) # ex. CS 241.
    courseID = models.IntegerField()
    sectionID = models.CharField(max_length=30, primary_key=True)
    sectionName = models.CharField(max_length=20) # part of PK
    instructor = models.CharField(max_length=50)

class Book(models.Model):
    isbn = models.CharField(max_length=30,)
    author = models.CharField(max_length=100)
    required = models.CharField(max_length=50, null=True)
    broncoPrice = models.DecimalField(max_digits=10, decimal_places=2)
    binding = models.CharField(max_length=15, null=True)
    edition = models.CharField(max_length=4, null=True)
    # going to be looking for book via courseName and sectionName
    courseName = models.CharField(max_length=30)
    sectionName = models.CharField(max_length=30)

class ListedBook(models.Model):
    private_id = models.IntegerField(primary_key=True)
    isbn = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    condition = models.CharField(max_length=50)
