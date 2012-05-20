from optparse import make_option
from django.core.management.base import NoArgsCommand
import pickle
from app.models import Course

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
				newCourseID = courses['id']
				newCourse = Course(courseID=newCourseID, name=newCourseName)
				newCourse.save()
