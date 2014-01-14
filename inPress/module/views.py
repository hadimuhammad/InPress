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

def instructoraddclass(request):
    if (request.method == 'POST'):
        try:
            a = Courses.objects.get(CourseCode = request.POST['classCode'])
            return HttpResponseRedirect('/instructor/index')
        except Courses.DoesNotExist:
            b = Courses(CourseName=request.POST['className'], CourseCode=request.POST['classCode'])
            b.save()
            return HttpResponseRedirect('/instructor/index')
    return render_to_response('instructoraddclass.html', RequestContext(request, {}))  