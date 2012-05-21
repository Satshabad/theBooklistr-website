# This script will insert all the courses from courseData.txt 
# into the app_course table.

from optparse import make_option
from django.core.management.base import NoArgsCommand
import pickle
from app.models import Book
from app.models import Course

class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        data = pickle.load(open('courseData.txt'))
        option_list = NoArgsCommand.option_list + (make_option('--verbose', action='store_true'),)

        correctBooks = Course.objects.filter(name = request.GET['q'], sectionID = request.GET['s'])
        for book in CorrectBooks :
            print book
