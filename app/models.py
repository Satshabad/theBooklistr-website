from django.db import models

class Section(models.Model):
    courseName = models.CharField(max_length=30) # ex. CS 241.
    sectionID = models.CharField(max_length=30, primary_key=True)
    sectionName = models.CharField(max_length=20) # E-01
    instructor = models.CharField(max_length=150)
    quarterName = models.CharField(max_length=150)


class ListedBook(models.Model):
    secret_key = models.CharField(max_length=32)
    isbn = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=5)
    timeListed = models.DateTimeField(auto_now_add=True)

class Book(models.Model):
    isbn = models.CharField(max_length=30)
    sectionID = models.CharField(max_length=30)
    required = models.CharField(max_length=50, null=True)
    broncoPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    edition = models.CharField(max_length=4, null=True)
    binding = models.CharField(max_length=15, null=True)
