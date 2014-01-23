# Some standard Django stuff
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from module.models import *
from django.shortcuts import render_to_response, render
from array import *
from django.core import serializers
 
 
def studentsignin(request):
    return render_to_response('studentsignin.html', RequestContext(request, {}))

def instructorsignin(request):
    return render_to_response('instructorsignin.html', RequestContext(request, {}))

def instructorindex(request):
    courses = Courses.objects.all()
    print courses
    return render_to_response('instructorindex.html', locals()) 

def removeclass(request):
    courses = Courses.objects.all()
    print courses
    if (request.method == 'POST'):
        print request.POST['courseToDelete']
        courseToDelete = Courses.objects.filter(CourseName=request.POST['courseToDelete'])
        print courseToDelete
        courseToDelete.delete()
        return HttpResponseRedirect('index.html')
    return render_to_response('removeclass.html', locals()) 

def addclass(request):
    if (request.method == 'POST'):
        try:
            a = Courses.objects.get(CourseName = request.POST['className'])
            return HttpResponseRedirect('/instructor/index.html')
        except Courses.DoesNotExist:
            b = Courses(CourseName=request.POST['className'], CourseCode=request.POST['classCode'])
            b.save()
            return HttpResponseRedirect('/instructor/index.html')
    return render_to_response('addclass.html', RequestContext(request, {}))

def course(request):
    courses = Courses.objects.all()
    if (request.method == 'GET'):
        myCourse = request.GET['courseInfo']
        courseName = Courses.objects.filter(CourseName=myCourse)
        assessments = Assessment.objects.filter(course = courseName)
        ListOfAssessments = serializers.serialize("json", assessments)
        QuestionData = serializers.serialize("json", AssessmentData.objects.filter(Assessment=assessments))
        print QuestionData
        print ListOfAssessments
    return render_to_response('course.html', locals()) 

def addassessment(request):
    courses = Courses.objects.all()
    if (request.method == 'GET'):
        myCourse = request.GET['course']
    if (request.method == 'POST'):
        myCourse = request.POST['course']
        print myCourse
        assessmentToAdd = request.POST ['AssessmentName']
        try:
            course = Courses.objects.get(CourseName = myCourse)
            a = Assessment.objects.get(name = assessmentToAdd, course=course)
            return HttpResponseRedirect('/instructor/course.html?courseInfo='+myCourse)
        except Assessment.DoesNotExist:
            a = Courses.objects.get(CourseName = myCourse)
            b = Assessment(name = assessmentToAdd, course=a)
            b.save()
            return HttpResponseRedirect('/instructor/course.html?courseInfo='+myCourse)
    return render_to_response('addassessment.html', locals()) 

def removeassessment(request):
    courses = Courses.objects.all()
    if (request.method == 'GET'):
        myCourse = request.GET['course']
        courseName = Courses.objects.filter(CourseName=myCourse)
        assessments = Assessment.objects.filter(course = courseName)
    if (request.method == 'POST'):
        myCourse = request.POST['course']
        courseName = Courses.objects.filter(CourseName=request.POST['course'])
        assessmentToDelete = Assessment.objects.filter(name=request.POST['assessmentToDelete'], course=courseName)
        assessmentToDelete.delete()
        return HttpResponseRedirect('/instructor/course.html?courseInfo='+myCourse)
    return render_to_response('removeassessment.html', locals()) 



def addquestion(request):
    courses = Courses.objects.all()
    if (request.method == 'GET'):
        myCourse = request.GET['course']
        myAssessment = request.GET['assessment']
        courseName = Courses.objects.filter(CourseName=myCourse)
        assessment = Assessment.objects.get(name=myAssessment, course = courseName)
    if (request.method == 'POST'):
        courseName = Courses.objects.filter(CourseName=request.POST['course'])
        assessment = Assessment.objects.get(name = request.POST['assessment'], course=courseName)
        print request.POST
        if (request.POST['SAAns'] != ''):
            questionSA = AssessmentData(Assessment = assessment, Question_Type="SA", Question_Data=request.POST['questionText'], Question_Answer=request.POST['SAAns'])
            questionSA.save()
            return HttpResponseRedirect('/instructor/course.html?courseInfo='+request.POST['course'])
        else:
            question = AssessmentData(Assessment = assessment, Question_Type="MC", Question_Data=request.POST['questionText'], 
                Question_Answer=request.POST['MCRadio'], ChoiceA = request.POST['MC1Ans'], ChoiceB = request.POST['MC2Ans'], 
                ChoiceC = request.POST['MC3Ans'], ChoiceD = request.POST['MC4Ans'], ChoiceE=request.POST['MC5Ans'])
            question.save()

            return HttpResponseRedirect('/instructor/course.html?courseInfo='+request.POST['course'])
    return render_to_response('addquestion.html', locals()) 

def studentcourse(request):
    courses = Courses.objects.all()
    print courses
    return render_to_response('studentcourse.html', locals())


def studentindex(request):
    courses = Courses.objects.all()
    print courses
    return render_to_response('studentindex.html', locals()) 
