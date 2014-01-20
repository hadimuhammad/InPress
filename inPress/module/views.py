# Some standard Django stuff
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from module.models import *
from django.shortcuts import render_to_response, render
from array import *
 
 
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
        print assessments
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

def studentchoosecourse(request):
    courses = Courses.objects.all()
    print courses
    return render_to_response('studentchoosecourse.html', locals())