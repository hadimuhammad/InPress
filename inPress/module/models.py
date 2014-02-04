from django.db import models

class Courses (models.Model):
	CourseName = models.CharField(max_length=200)
	CourseCode = models.CharField(max_length=200)
	def __unicode__(self):
		return self.CourseName
		
class Students (models.Model):
	StudentNumber = models.CharField(max_length=200)
	CourseName = models.ForeignKey (Courses)
	def __unicode__(self):
		return self.StudentNumber

class AssessmentManager(models.Manager):
    def get_by_natural_key(self, name, course):
        return self.get(name=name, course=course)

class Assessment (models.Model):
	objects = AssessmentManager()
	name = models.CharField(max_length=200)
	course = models.ForeignKey(Courses)
	post_date = models.DateField()
	def natural_key(self):
		return (self.name, self.course)
	def __unicode__(self):
		return self.name
	class Meta:
		unique_together = (('name', 'course'),)

class AssessmentData (models.Model):
	Assessment = models.ForeignKey (Assessment)
	Question_Number = models.CharField(max_length = 10)
	Question_Type = models.CharField(max_length=10)
	Question_Data = models.CharField(max_length=200)
	Question_Answer = models.CharField(max_length=200)
	ChoiceA = models.CharField(max_length=200)
	ChoiceB = models.CharField(max_length=200)
	ChoiceC = models.CharField(max_length=200)
	ChoiceD = models.CharField(max_length=200)
	ChoiceE = models.CharField(max_length=200)
	def __unicode__(self):
		return self.Question_Data

