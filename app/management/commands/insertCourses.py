# This script will insert all the courses from courseData.txt 
# into the app_course table.

from optparse import make_option
from django.core.management.base import BaseCommand
import pickle
from app.models import Section

class Command(BaseCommand):

    def handle(self, *args, **options):
		data = pickle.load(open(str(args[0])))


		for dept in data:
			for courses in dept['courses']:
				newCourseName = courses['name']
				for section in courses['sections']:
					newSectionID = section['id']
					newSectionName = section['name']
					newInstructor = section['instructor']
					newCourse = Section(
                        courseName = newCourseName, 
						sectionID = newSectionID, 
						sectionName = newSectionName, 
						instructor = newInstructor)
					newCourse.save()
