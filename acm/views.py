from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import config
import inspect
from django.shortcuts import redirect
from django.contrib import messages
from .models import School
from django.contrib.auth.decorators import login_required
from .forms import SchoolForm

# Create your views here.

# Function to render templates
def render_template(context, request, template_name = "default"):
	page_name = template_name
	if template_name == "default":
		template_name = page_name = inspect.stack()[1][3] #Use calling function's name if temp is not set or is deault
	template_name = "acm/" + template_name + ".html"
	template_obj = loader.get_template(template_name)
	return HttpResponse(template_obj.render(context, request))

@login_required(login_url='/login')	
def index(request):
	schools = School.objects.filter(verified=True)
	context = {
		'title': config.app + ' | Cargo Space Challenge',
		'page': 'acm',
		'schools': schools,
	}
	return render_template(context, request)

@login_required(login_url='/login')
def schools(request):
	
	if request.method == 'POST':
		return doAddSchool(request)
		
	schools = School.objects.all()
	context = {
		'title': config.app + ' | Cargo Space Challenge Problemset', 
		'page': 'school',
		'schools': schools,
	}
	return render_template(context, request, template_name = "school")

def doAddSchool(request):
	if request.method == 'POST':
		school_form = SchoolForm(data=request.POST)
		if school_form.is_valid():
			school_form.save()
			return redirect(schools)
		else:
			messages.info(request, messages.ERROR, "Please check the inputs and try again")
			return redirect(schools)
	else:
		return redirect(schools)