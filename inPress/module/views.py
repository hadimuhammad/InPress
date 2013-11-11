# Some standard Django stuff
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Context, loader
from module.models import *
from django.shortcuts import render_to_response, render
# list of mobile User Agents
mobile_uas = [
        'w3c ','acs-','alav','alca','amoi','audi','avan','benq','bird','blac',
        'blaz','brew','cell','cldc','cmd-','dang','doco','eric','hipt','inno',
        'ipaq','java','jigs','kddi','keji','leno','lg-c','lg-d','lg-g','lge-',
        'maui','maxo','midp','mits','mmef','mobi','mot-','moto','mwbp','nec-',
        'newt','noki','oper','palm','pana','pant','phil','play','port','prox',
        'qwap','sage','sams','sany','sch-','sec-','send','seri','sgh-','shar',
        'sie-','siem','smal','smar','sony','sph-','symb','t-mo','teli','tim-',
        'tosh','tsm-','upg1','upsi','vk-v','voda','wap-','wapa','wapi','wapp',
        'wapr','webc','winw','winw','xda','xda-'
        ]
 
mobile_ua_hints = [ 'SymbianOS', 'Opera Mini', 'iPhone', 'Android' ]
 
 
def mobileBrowser(request):
    ''' Super simple device detection, returns True for mobile devices '''
 
    mobile_browser = False
    ua = request.META['HTTP_USER_AGENT'].lower()[0:4]
 
    if (ua in mobile_uas):
        mobile_browser = True
    else:
        for hint in mobile_ua_hints:
            if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                mobile_browser = True
 
    return mobile_browser
 
 
def index(request):
    '''Render the index page'''
 
    if mobileBrowser(request):
        t = loader.get_template('mobile/m_index.html')
    else:
        t = loader.get_template('index.html')
 
    c = Context( { }) # normally your page data would go here
 
    return HttpResponse(t.render(c))

def questiontype (request):
	print request
	assessment = Assessment.objects.get(name = request.GET['assessment'])
	if (mobileBrowser (request)):
                return render_to_response('mobile/m_questiontype.html', locals())
        else:
                return render_to_response('questiontype.html', locals())

def questions(request):
        if (request.method == 'POST'):
                assessment= Assessment.objects.get(name = request.POST['assessment'])
                if (mobileBrowser (request)):
                        return render_to_response('mobile/m_questions.html',locals())
                else:
                        return render_to_response('questions.html',locals())
        if (mobileBrowser (request)):
                return render_to_response('mobile/m_questions.html', RequestContext(request, {}))
        else:
                return render_to_response('questions.html', RequestContext(request, {}))

# Student Index page
# stuIndex.html // m_stuIndex.html
def stuIndex(request):
    '''Render the Student index page'''

    if mobileBrowser(request):
        student_template = loader.get_template('mobile/m_stuIndex.html')
    else:
        student_template  = loader.get_template('stuIndex.html')

    c = Context( { }) # normally your page data would go here

    return HttpResponse(student_template.render(c))
def addassessment (request):
        isMobile = False
        if (mobileBrowser (request)):
                isMobile = True
        else:
                isMobile = False

        if (request.method == 'POST'):
                try:
                        a = Assessment.objects.get(name = request.POST['assessmentname'])
                        return HttpResponseRedirect('/addassessment')
                except Assessment.DoesNotExist:
                        b = Assessment(name=request.POST['assessmentname'])
                        b.save()
                        return HttpResponseRedirect('/instructor')
                
        if (isMobile):
                return render_to_response('mobile/m_addassessment.html', RequestContext(request, {}))
        else:
                return render_to_response('addassessment.html', RequestContext(request, {}))

def addmcquestion (request):
        assessment = Assessment.objects.get(name = request.GET['assessment'])
        if (mobileBrowser (request)):
                return render_to_response('mobile/m_addmcquestion.html', locals())
        else:
                return render_to_response('addmcquestion.html',locals())

def addnaquestion (request):
        assessment = Assessment.objects.get(name = request.GET['assessment'])
        if (mobileBrowser (request)):
                return render_to_response('mobile/m_addnaquestion.html', locals())
        else:
                return render_to_response('addnaquestion.html',locals())

def instructor (request):
	if (mobileBrowser (request)):
                return render_to_response('mobile/m_instructor.html', locals())
        else:
                return render_to_response('instructor.html',locals())

def addsaquestion (request): 
	assessment = Assessment.objects.get(name = request.GET['assessment'])
	if (mobileBrowser (request)):
                return render_to_response('mobile/m_addsaquestion.html', locals())
        else:
                return render_to_response('addsaquestion.html',locals())
def removequestions(request):
	if (request.method == 'GET'):
		assessment = Assessment.objects.get(name = request.GET['assessment'])
		assessmentData = AssessmentData.objects.filter(Assessment = assessment)
	if (request.method == 'POST'):
		assessment = Assessment.objects.get(name = request.POST['assessment'])
		a = AssessmentData.objects.get(Assessment = assessment, Question_Number = request.POST['question'])
		a.delete()
		return HttpResponseRedirect('/') 	
	if (mobileBrowser (request)):
		return render_to_response('mobile/m_removequestions.html', locals())
        else:
                return render_to_response('removequestions.html',locals())

def removeassessment (request):
        assessment = Assessment.objects.all()
        isMobile = False
        if (mobileBrowser (request)):
                isMobile = True
        else:
                isMobile = False
        
        if (request.method == 'POST'):
                a = Assessment.objects.get(name = request.POST['assessment'])
                a.delete()
                return HttpResponseRedirect('/removeassessment')        
        
        if (isMobile):
                return render_to_response('mobile/m_removeassessment.html', locals())
        else:
                return render_to_response('removeassessment.html',locals())

def viewquestions(request):
	assessment = Assessment.objects.get(name = request.GET['assessment'])
	assessmentData = AssessmentData.objects.filter(Assessment = assessment)
	if (mobileBrowser (request)):
                return render_to_response('mobile/m_viewquestions.html', locals())
        else:
                return render_to_response('viewquestions.html', locals())
	
def addquestion (request):
        if (request.method == 'GET'):
		assessment = Assessment.objects.get(name = request.GET['assessment'])
        if (request.method == 'POST'):
                a = Assessment.objects.get(name = request.POST['assessment'])
                numQuestions = AssessmentData.objects.filter(Assessment =a).count()+1
                if (request.POST['Question_Type'] == "Multiple Choice"):
			b = AssessmentData(Assessment = a,  Question_Number=numQuestions, Question_Type=request.POST['Question_Type'], Question_Data=request.POST['QuestionContent'], Question_Answer="Ignore Me")
			b.save()
			c = MCQuestionData(Assessment = a, AssessmentData = b, Choice_Type='a', Choice_Content=request.POST['QuestionAnswer1'])
			c.save()
			d = MCQuestionData(Assessment = a, AssessmentData = b, Choice_Type='b', Choice_Content=request.POST['QuestionAnswer2'])
                        d.save()
			e = MCQuestionData(Assessment = a, AssessmentData = b, Choice_Type='c', Choice_Content=request.POST['QuestionAnswer3'])
                        e.save()
			f = MCQuestionData(Assessment = a, AssessmentData = b, Choice_Type='d', Choice_Content=request.POST['QuestionAnswer4'])
                        f.save()
			g = MCQuestionData(Assessment = a, AssessmentData = b, Choice_Type='e', Choice_Content=request.POST['QuestionAnswer5'])
                        g.save()
			return HttpResponseRedirect('/instructor')
		else:
			b = AssessmentData(Assessment = a,  Question_Number=numQuestions, Question_Type=request.POST['Question_Type'], Question_Data=request.POST['QuestionContent'], Question_Answer=request.POST['QuestionAnswer'])
                	b.save()
                	return HttpResponseRedirect('/instructor')

        if (mobileBrowser (request)):
                return render_to_response('mobile/m_addquestion.html', locals())
        else:
                return render_to_response('addquestion.html', locals())

def viewassessments (request):
        isMobile = False
        if (mobileBrowser (request)):
                isMobile = True
        else:
                isMobile = False
        
        assessments = Assessment.objects.all()
        
        if (isMobile):
                return render_to_response('mobile/m_viewassessments.html', locals())
        else:
                return render_to_response('viewassessments.html', locals()) 

def addcourses (request):

        isMobile = False
        if (mobileBrowser (request)):
                isMobile = True
        else:
                isMobile = False


        if (request.method == 'POST'):
                course_name  = Courses(CourseName=request.POST['coursename'])
                course_name.save()

        if (isMobile):
                return render_to_response('mobile/m_addcourses.html', RequestContext(request, {}))
        else:
                return render_to_response('addcourses.html', RequestContext(request, {}))

def removecourses (request):
        courses = Courses.objects.all()
        isMobile = False
        if (mobileBrowser (request)):
                isMobile = True
        else:
                isMobile = False

        if (request.method == 'POST'):
                course_name = Courses.object.filter(name=request.POST['courses'])
                course_name.delete()
                course_name.save()
                if (isMobile):
                        return render_to_response('mobile/m_removecourses.html', RequestContext(request, {}))
                else:
                        return render_to_response('removecourses.html', RequestContext(request, {}))
        if (isMobile):
                return render_to_response('mobile/m_removecourses.html', locals())
        else:
                return render_to_response('removecourses.html',locals())
