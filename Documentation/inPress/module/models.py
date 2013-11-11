from django.db import models

class Assessment (models.Model):
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class AssessmentData (models.Model):
	Assessment = models.ForeignKey (Assessment)
	Question_Number = models.CharField(max_length = 10)
	Question_Type = models.CharField(max_length=10)
	Question_Data = models.CharField(max_length=200)
	Question_Answer = models.CharField(max_length=200)
	def __unicode__(self):
		return self.Question_Data

class MCQuestionData (models.Model):
	Assessment = models.ForeignKey (Assessment)
	AssessmentData = models.ForeignKey (AssessmentData)
	Choice_Type = models.CharField(max_length=10)
	Choice_Content = models.CharField(max_length=200)
	def __unicode__(self):	
		return self.Question_Number

class Courses (models.Model):
        CourseName = models.CharField(max_length=200)
        CourseCode = models.CharField(max_length=200)
        def __unicode__(self):
                return self.CourseName
