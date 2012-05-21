# This script will insert all the courses from courseData.txt 
# into the app_course table.

from optparse import make_option
from django.core.management.base import NoArgsCommand
import pickle
from app.models import Book

class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        data = pickle.load(open('courseData.txt'))
        option_list = NoArgsCommand.option_list + (make_option('--verbose', action='store_true'),)

        for dept in data:
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
