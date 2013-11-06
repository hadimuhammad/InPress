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
        t = loader.get_template('m_index.html')
    else:
        t = loader.get_template('index.html')
 
    c = Context( { }) # normally your page data would go here
 
    return HttpResponse(t.render(c))

# Student Index page
# stuIndex.html // m_stuIndex.html
def stuIndex(request):
    '''Render the Student index page'''

    if mobileBrowser(request):
        student_template = loader.get_template('m_stuIndex.html')
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
			return HttpResponseRedirect('/')
		
	if (isMobile):
		return render_to_response('m_addassessment.html', RequestContext(request, {}))
	else:
		return render_to_response('addassessment.html', RequestContext(request, {}))
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
                return render_to_response('m_removeassessment.html', locals())
        else:
                return render_to_response('removeassessment.html',locals())

def addquestion (request):
	isMobile = False
	if (mobileBrowser (request)):
		isMobile = True
	else:
		isMobile = False

	if (request.method == 'POST'):
  		b = AssessmentData(Question_Number=request.POST['Question_Number'], Question_Type=request.POST['Question_Type'], Question_Data=request.POST['Question_Data'], Question_Answer=request.POST['Question_Answer'])
                b.save()

 	if (isMobile):
		return render_to_response('m_addquestion.html', RequestContext(request, {}))
	else:
		return render_to_response('addquestion.html', RequestContext(request, {}))

def viewassessments (request):
	isMobile = False
	if (mobileBrowser (request)):
		isMobile = True
	else:
		isMobile = False
	
	assessments = Assessment.objects.all()
	
	if (isMobile):
		return render_to_response('m_viewassessments.html', locals())
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
                return render_to_response('m_addcourses.html', RequestContext(request, {}))
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
                        return render_to_response('m_removecourses.html', RequestContext(request, {}))
                else:
                        return render_to_response('removecourses.html', RequestContext(request, {}))
        if (isMobile):
                return render_to_response('m_removecourses.html', locals())
        else:
                return render_to_response('removecourses.html',locals())

