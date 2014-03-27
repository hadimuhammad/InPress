# Some standard Django stuff
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from module.models import *
from django.shortcuts import render_to_response, render
from array import *
from django.core import serializers
from datetime import date
from urlparse import urlparse
from django.db.models import Count
from .forms import UploadFileForm
 
def studentsignin(request):
    if (request.method == 'POST'):
        print request.POST['studentnumber']
        course = Students.objects.filter (StudentNumber = request.POST['studentnumber']).values("CourseName")
        if (course.count() < 1):
            return HttpResponseRedirect('/')
        else:
            return studentindex(request)
            #return HttpResponseRedirect('/student/index.html?studentnumber='+request.POST['studentnumber'])
    return render_to_response('studentsignin.html', RequestContext(request, {}))

def instructorsignin(request):
    return render_to_response('instructorsignin.html', RequestContext(request, {}))

def instructorindex(request):
    #check the instructor credentials: 
    name = request.POST.get('username')
    if (name):
        instructor_user = Instructor.objects.values_list('username', flat=True)
        instructor_pas = Instructor.objects.values_list('password', flat=True)
        instructor_pass = '-'.join([str(i) for i in instructor_pas.order_by('?')[:4]])
        if (request.POST["password"] == instructor_pass):
            courses = Courses.objects.all()
            print courses
            return render_to_response('instructorindex.html', locals()) 
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
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
    if (request.method == 'GET'):
        courses = Courses.objects.all()
    if (request.method == 'POST'):
        print request
        try:
            a = Courses.objects.get(CourseName = request.POST['className'])
            return HttpResponseRedirect('/instructor/index.html')
        except Courses.DoesNotExist:
            b = Courses(CourseName=request.POST['className'], CourseCode=request.POST['classCode'])
            b.save()
            form = UploadFileForm(request.POST, request.FILES)
            dataFile = request.FILES['classList']
            course = Courses.objects.get(CourseName = request.POST['className'])
            for eachLine in dataFile.__iter__():
                eachLine = eachLine.replace('\n', '')
                a = Students(StudentNumber=eachLine, CourseName=course)
                a.save()
            dataFile.close()
            return HttpResponseRedirect('/instructor/index.html')
    return render_to_response('addclass.html', RequestContext(request, {}))

def inclass (request):
    print request
    last = "false"
    courses = Courses.objects.all()
    myCourse = request.POST['course']
    questNum = int(request.POST['questNum'])
    if (questNum < 1):
        questNum = 1
    courseName = Courses.objects.filter(CourseName=myCourse)
    assessment = Assessment.objects.filter(name=request.POST['assessment'], course=courseName)
    assessments = Assessment.objects.filter(pk__in=assessment).order_by('created_time')
    Assessmentdata = AssessmentData.objects.filter(Assessment__in=assessments)
    numQuestions = Assessmentdata.count()
    if (questNum > numQuestions):
        questNum = numQuestions
        last = "true"
    ListOfAssessments = serializers.serialize("json", assessments)
    QuestionData = serializers.serialize("json", Assessmentdata)
    Answers = serializers.serialize("json", StudentAnswers.objects.filter(AssessmentData__in=Assessmentdata))
    print QuestionData
    AssessmentDatas = AssessmentData.objects.filter(Assessment = assessment)
    numOfQuestions = AssessmentDatas.count()
    numOfStudents = Students.objects.filter (CourseName=courseName).count()
    numOfQuestionsComplete = StudentAnswers.objects.filter(AssessmentData__in = AssessmentDatas).count()
    numOfStudentsComplete  = numOfQuestionsComplete // numOfQuestions
    AssessmentDataSA = AssessmentData.objects.filter(Assessment = assessment, Question_Type="SA")
    AnswerGroups = StudentAnswers.objects.filter(AssessmentData__in=AssessmentDataSA).values('Answer', 'AssessmentData').annotate(numStudents=Count('Answer')).order_by('-numStudents')
    print AnswerGroups
    return render_to_response('inclass.html', locals()) 
    
def course(request):
    courses = Courses.objects.all()
    if (request.method == 'GET'):
        myCourse = request.GET['courseInfo']
        courseName = Courses.objects.filter(CourseName=myCourse)
        assessments = Assessment.objects.filter(course = courseName).order_by('created_time')
        posting = Assessment.objects.filter(course=courseName).values("post")
        ListOfAssessments = serializers.serialize("json", assessments)
        QuestionData = serializers.serialize("json", AssessmentData.objects.filter(Assessment__in=assessments))
    if (request.method == 'POST'):
        my_param = request.POST.get('postIT')
        if (my_param):
            isPost  = False
            if (request.POST['postIT'] == "false"):
                isPost = False
            else:
                isPost = True
            myCourse = request.POST['course']
            assessmentToPost= request.POST['aToMod']
            course = Courses.objects.get(CourseName = myCourse)
            assessments = Assessment.objects.filter(course = course)
            a = Assessment.objects.filter(name = assessmentToPost, course=course).update(post=isPost)
            accordion = request.POST['accordionNumber']
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')+'#accordion'+accordion)
        else:
            assessmentToDelete = AssessmentData.objects.get(pk=request.POST['QuestionToRemove'])
            assessmentToDelete.delete()
            accordion = request.POST['accordionNumber']
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')+'#accordion'+accordion)
    return render_to_response('course.html', locals()) 

def addassessment(request):
    if (request.method == 'GET'):
        myCourse = request.GET['course']
        courses = Courses.objects.all()
    if (request.method == 'POST'):
        print request
        myCourse = request.POST['course']
        accordion = request.POST.get('accordionNumber')
        if (accordion is None):
            accordion = "-1"
        assessmentToAdd = request.POST ['AssessmentName']
        try:
            course = Courses.objects.get(CourseName = myCourse)
            a = Assessment.objects.get(name = assessmentToAdd, course=course)
            Assessment.objects.filter (name = assessmentToAdd, course=course).update(post_date=request.POST ['effectivedate'])
            return HttpResponseRedirect('/instructor/course.html?courseInfo='+myCourse+'#accordion'+accordion)
        except Assessment.DoesNotExist:
            a = Courses.objects.get(CourseName = myCourse)
            b = Assessment(name = assessmentToAdd, course=a, post_date=request.POST ['effectivedate'])
            b.save()
            return HttpResponseRedirect('/instructor/course.html?courseInfo='+myCourse+'#accordion'+accordion)
    return render_to_response('addassessment.html', locals()) 

def removeassessment(request):
    courses = Courses.objects.all()
    if (request.method == 'GET'):
        myCourse = request.GET['course']
        courseName = Courses.objects.filter(CourseName=myCourse)
        assessments = Assessment.objects.filter(course = courseName).order_by('created_time')
    if (request.method == 'POST'):
        myCourse = request.POST['course']
        courseName = Courses.objects.filter(CourseName=request.POST['course'])
        assessmentToDelete = Assessment.objects.filter(name=request.POST['assessmentToDelete'], course=courseName)
        assessmentToDelete.delete()
        return HttpResponseRedirect('/instructor/course.html?courseInfo='+myCourse)
    return render_to_response('removeassessment.html', locals()) 

def addquestion(request):
    if (request.method == 'GET'):
        courses = Courses.objects.all()
        myCourse = request.GET['course']
        myAssessment = request.GET['assessment']
        courseName = Courses.objects.filter(CourseName=myCourse)
        assessment = Assessment.objects.get(name=myAssessment, course = courseName)
        accordion = request.GET['accordionNumber']
        print accordion
    if (request.method == 'POST'):
        courseName = Courses.objects.filter(CourseName=request.POST['course'])
        assessment = Assessment.objects.get(name = request.POST['assessment'], course=courseName)
        accordion = request.POST['accordionNumber']
        print request.POST
        if (request.POST['SAAns'] != ''):
            questionSA = AssessmentData(Assessment = assessment, Question_Type="SA", Question_Data=request.POST['questionText'], Question_Answer=request.POST['SAAns'])
            questionSA.save()
            return HttpResponseRedirect('/instructor/course.html?courseInfo='+request.POST['course']+'#accordion'+accordion)
        else:
            question = AssessmentData(Assessment = assessment, Question_Type="MC", Question_Data=request.POST['questionText'], 
                Question_Answer=request.POST['MCRadio'], ChoiceA = request.POST['MC1Ans'], ChoiceB = request.POST['MC2Ans'], 
                ChoiceC = request.POST['MC3Ans'], ChoiceD = request.POST['MC4Ans'], ChoiceE=request.POST['MC5Ans'])
            question.save()
            return HttpResponseRedirect('/instructor/course.html?courseInfo='+request.POST['course']+'#accordion'+accordion)
    return render_to_response('addquestion.html', locals()) 

def data_analysis(request):
    course = request.GET['course']
    courses = Courses.objects.all()
    courseName = Courses.objects.filter(CourseName=course)
    assessment = request.GET['assessment']
    assessmentName = Assessment.objects.filter(name = assessment, course=courseName)
    ListOfAssessments = serializers.serialize("json", assessmentName)
    Assessmentdata = AssessmentData.objects.filter(Assessment__in=assessmentName)
    QuestionData = serializers.serialize("json", Assessmentdata)
    Answers = serializers.serialize("json", StudentAnswers.objects.filter(AssessmentData__in=Assessmentdata))
    print QuestionData
    AssessmentDatas = AssessmentData.objects.filter(Assessment = assessmentName)
    numOfQuestions = AssessmentDatas.count()
    numOfStudents = Students.objects.filter (CourseName=courseName).count()
    numOfQuestionsComplete = StudentAnswers.objects.filter(AssessmentData__in = AssessmentDatas).count()
    numOfStudentsComplete  = numOfQuestionsComplete // numOfQuestions
    AssessmentDataSA = AssessmentData.objects.filter(Assessment = assessmentName, Question_Type="SA")
    AnswerGroups = StudentAnswers.objects.filter(AssessmentData__in=AssessmentDataSA).values('Answer', 'AssessmentData').annotate(numStudents=Count('Answer')).order_by('-numStudents')
    print AnswerGroups
    return render_to_response('data_analysis.html', locals()) 

def checkStudentInList (student, studentList):
    for i in studentList:
        if (str(student) == str(i)):
            return True
    return False;

def viewclass (request):
    if (request.method == 'GET'):
        course = request.GET['course']
        courses = Courses.objects.all()
        courseName = Courses.objects.filter(CourseName=course)
        allEnrolledStudents = Students.objects.filter (CourseName=courseName)
        print allEnrolledStudents
        return render_to_response('viewclass.html', locals()) 
    if (request.method == 'POST'):
        course = request.POST ['course']
        studentlist = request.POST.getlist('students')
        courseName = Courses.objects.get (CourseName=course)
        AllEnrolledStudents = Students.objects.filter(CourseName=courseName)

        # Delete all students not in the new list
        for eachStudent in AllEnrolledStudents:
            isStudentInClass = checkStudentInList (eachStudent, studentlist)
            if (not (isStudentInClass)):
                print "Deleting Student Number: "+str(eachStudent)
                studentToDelete = Students.objects.filter(StudentNumber=eachStudent, CourseName=courseName)
                studentToDelete.delete()

        # Add all students not enrolled
        for student in studentlist:
            try:
                entry = Students.objects.get(StudentNumber = student, CourseName=courseName)
            except Students.DoesNotExist:
                print "Adding Student Number: "+str(student)
                add = Students(StudentNumber = student, CourseName=courseName)
                add.save()
        return HttpResponseRedirect('/instructor/course.html?courseInfo='+course)

def studentcourse(request):
    if (request.method == 'POST'):
        studentnumber = request.POST['studentnumber']
        mycourses = Students.objects.filter (StudentNumber = request.POST['studentnumber']).values("CourseName")
        courses = Courses.objects.filter (pk__in=mycourses)
        myCourse = request.POST['course']
        courseName = Courses.objects.filter(CourseName=myCourse)
        assessments = Assessment.objects.filter(course = courseName, post = "true", post_date = date.today())
        ListOfAssessments = serializers.serialize("json", assessments)
        QuestionData = serializers.serialize("json", AssessmentData.objects.filter(Assessment__in=assessments))
    return render_to_response('studentcourse.html', locals()) 

def studentcoursehistory(request):
    if (request.method == 'POST'):
        studentnumber = request.POST['studentnumber']
        mycourses = Students.objects.filter (StudentNumber = request.POST['studentnumber']).values("CourseName")
        courses = Courses.objects.filter (pk__in=mycourses)
        myCourse = request.POST['course']
        courseName = Courses.objects.filter(CourseName=myCourse)
        assessments = Assessment.objects.filter(course = courseName, post = "true", post_date__lte = date.today())
        ListOfAssessments = serializers.serialize("json", assessments)
        QuestionData = serializers.serialize("json", AssessmentData.objects.filter(Assessment__in=assessments))
    return render_to_response('studentCourseHistory.html', locals())

def studentindex(request):
    studentnumber = request.POST['studentnumber']
    mycourses = Students.objects.filter (StudentNumber = request.POST['studentnumber']).values("CourseName")
    courses = Courses.objects.filter (pk__in=mycourses)
    return render_to_response('studentindex.html', locals()) 

def getViewAssessment (request):
    myCourse = request.POST['course']
    assessmentPK = request.POST ['AssessmentPK']
    assessmentName = Assessment.objects.get(pk =assessmentPK)
    QuestionNum = request.POST['QuestionNum']
    assessments = Assessment.objects.filter(pk =assessmentPK)
    QuestionData = serializers.serialize("json", AssessmentData.objects.filter(Assessment__in=assessments))
    studentnumber = request.POST['studentnumber']
    mycourses = Students.objects.filter (StudentNumber = request.POST['studentnumber']).values("CourseName")
    courses = Courses.objects.filter (pk__in=mycourses)
    return render_to_response('viewassessment.html', locals()) 

def postAssessmentData (request, isEnd):
    assessmentData = AssessmentData.objects.filter (pk=request.POST ['assessmentDataPK'])
    assessmentDataPK = AssessmentData.objects.get (pk=request.POST ['assessmentDataPK'])
    myCourse = request.POST['course']
    course = Courses.objects.filter(CourseName = myCourse)
    students = Students.objects.get (StudentNumber = request.POST['studentnumber'], CourseName = course)
    answer = request.POST ['FinalAnswer']
    try:
        entry = StudentAnswers.objects.get(Students = students, AssessmentData = assessmentDataPK)
        StudentAnswers.objects.filter(Students = students, AssessmentData = assessmentDataPK).update (Answer = answer)
    except StudentAnswers.DoesNotExist:
        add = StudentAnswers(Students = students, AssessmentData = assessmentDataPK, Answer = answer)
        add.save()
    if (isEnd == True):
        return studentcourse(request)
        #return HttpResponseRedirect('/student/course.html?courseInfo='+request.POST['course']+'&studentnumber='+request.POST['studentnumber'])
    else:
        return 0;

def viewassessment(request):
    if (request.method == 'POST'):
	isEnd = request.POST.get('isEnd')
        answer = request.POST.get('FinalAnswer')
        if (answer):
            print request.POST['FinalAnswer']
        if (isEnd):
            if (isEnd == "true"):
                return postAssessmentData(request, True);
            else:
                postAssessmentData (request, False);
                return getViewAssessment(request); 
        else:
            return getViewAssessment(request);
def viewassessmentanswers(request):
    studentnumber = request.GET['studentnumber']
    mycourses = Students.objects.filter (StudentNumber = request.GET['studentnumber']).values("CourseName")
    courses = Courses.objects.filter (pk__in=mycourses)
    print request
    if (request.method == 'GET'):
        myCourse = request.GET['course']
        courseName = Courses.objects.filter(CourseName=myCourse)
        assessmentPK = request.GET ['AssessmentPK']
        assessments = Assessment.objects.filter(pk = assessmentPK)
        assessmentName = Assessment.objects.get(pk =assessmentPK)
        QuestionNum = request.GET['QuestionNum']
        ListOfAssessments = serializers.serialize("json", assessments)
        StudentAnswer = serializers.serialize("json", StudentAnswers.objects.filter(Students__in=studentnumber))
        QuestionData = serializers.serialize("json", AssessmentData.objects.filter(Assessment__in=assessments))
    if (request.method == 'POST'):
        assessmentToDelete = AssessmentData.objects.get(pk=request.POST['QuestionToRemove'])
        assessmentToDelete.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render_to_response('viewassessmentanswers.html', locals()) 

def studentcheckanswer (request):
    return render_to_response('studentcheckanswer.html', locals())

