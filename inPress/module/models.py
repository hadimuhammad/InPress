from django.db import models

# class admin(models.Model):
# 	adminID = models.CharField(max_length=10)
# 	adminPW = models.CharField(max_length=20)
# 	def __unicode__(self):
# 		return self.adminID

# class instructor(models.Model):
# 	instructorID = models.CharField(max_length=10)
# 	instructorPW = models.CharField(max_length=20)
# 	def __unicode__(self):
# 		return self.instructorID

class Courses (models.Model):
	CourseName = models.CharField(max_length=200)
	CourseCode = models.CharField(max_length=200)
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.CourseName		
		
class Students (models.Model):
	StudentNumber = models.CharField(max_length=200)
	CourseName = models.ForeignKey (Courses)
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.StudentNumber

class Instructor (models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	def __unicode__(self):
		return self.username

class AssessmentManager(models.Manager):
    def get_by_natural_key(self, name, course):
        return self.get(name=name, course=course)

class Assessment (models.Model):
	objects = AssessmentManager()
	name = models.CharField(max_length=200)
	course = models.ForeignKey(Courses)
	post_date = models.DateField()
	post = models.BooleanField(default=False)
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

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
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.Question_Data

class StudentAnswers (models.Model):
	Students = models.ForeignKey (Students)
	AssessmentData = models.ForeignKey (AssessmentData)
	Answer = models.CharField(max_length=200)
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)