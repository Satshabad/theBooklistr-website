# This script will insert all the courses from courseData.txt 
# into the app_course table.
from django.db import transaction
from optparse import make_option
from django.core.management.base import BaseCommand
import pickle
from app.models import Book, Section

class Command(BaseCommand):

    help = "pass in a file with the pickled data to insert"
    
    @transaction.commit_manually
    def handle(self, *args, **options):
        try:

            data = pickle.load(open(str(args[0])))
            Section.objects.all().delete()
            Book.objects.all().delete()
            for quarter in data:
                for dept in quarter['departments']:
                    for courses in dept['courses']:
                        newCourseName = courses['name']

                        for section in courses['sections']:
                            newSectionName = section['name']
                            newSectionID = section['id']

                            for book in section['books']:
                                newISBN = book['ISBN']
                                newAuthor = book['author']
                                newBinding = book['binding']
                                newPrice = book['broncoListPrice']
                                newEdition = book['edition']
                                newRequired = book['isRequired']
                                newtitle = book['title']

                                newBook = Book(
                                    isbn = newISBN,
                                    sectionID = newSectionID,
                                    required = newRequired,
                                    broncoPrice = newPrice,
                                    author = newAuthor,
                                    edition = newEdition,
                                    binding = newBinding,
                                    title = newtitle
                                )
                                newBook.save()
                                print newBook
                            
            for quarter in data:
                for dept in quarter['departments']:
                    for courses in dept['courses']:
                        newCourseName = courses['name']
                        for section in courses['sections']:
                            newSectionID = section['id']
                            newSectionName = section['name']
                            newInstructor = section['instructor']
                            newQuartername = quarter['name']
                            newCourse = Section(
                                quarterName = newQuartername, 
                                courseName = newCourseName, 
                                sectionID = newSectionID, 
                                sectionName = newSectionName, 
                                instructor = newInstructor)
                            newCourse.save()
        except:
            print 'uh oh something went wrong'
            transaction.rollback()
        else:
            transaction.commit()
