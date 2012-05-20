# This script will insert all the courses from courseData.txt 
# into the app_course table.

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
				for section in courses['sections']:
					newSectionID = section['id']
					newSectionName = section['name']
					newInstructor = section['instructor']
					newCourse = Course(name = newCourseName, 
						courseID = newCourseID, 
						sectionID = newSectionID, 
						sectionName = newSectionName, 
						instructor = newInstructor)
					newCourse.save()
