from django.db import models

# course should be section
class Section(models.Model):
    courseName = models.CharField(max_length=30) # ex. CS 241.
    sectionID = models.CharField(max_length=30, primary_key=True)
    sectionName = models.CharField(max_length=20) # E-01
    instructor = models.CharField(max_length=150)
    quarterName = models.CharField(max_length=150)

#class Book(models.Model):
#    going to be looking for book via courseName and sectionName
#    sectionID = models.CharField(max_length=30, primary_key=True)
#    courseName = models.CharField(max_length=30)
#    sectionName = models.CharField(max_length=30)

#class ListedBook(models.Model):
#    private_id = models.IntegerField(primary_key=True)
#    isbn = models.CharField(max_length=30)
#    email = models.CharField(max_length=100)
#    price = models.DecimalField(max_digits=10, decimal_places=4)
#    condition = models.CharField(max_length=50)

# ideas
class ListedBook(models.Model):
    secret_key = models.CharField(max_length=32)
    isbn = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=5)
    
    def __unicode__(self):
        return u"%s" % self.email

class Book(models.Model):
    isbn = models.CharField(max_length=30)
    sectionID = models.CharField(max_length=30)
    required = models.CharField(max_length=50, null=True)
    broncoPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    edition = models.CharField(max_length=4, null=True)
    binding = models.CharField(max_length=15, null=True)
