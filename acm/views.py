from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import config
import inspect
from django.shortcuts import redirect
from django.contrib import messages
from .models import School, Group, Member
from django.contrib.auth.decorators import login_required
from .forms import SchoolForm, MemberForm, GroupForm
from . import context_processors

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
		'title': config.app + ' | Cargo Space Challenge Registration',
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
		'title': config.app + ' | Cargo Space Challenge Schools', 
		'page': 'school',
		'schools': schools,
	}
	return render_template(context, request, template_name = "school")
	
@login_required(login_url='/login')
def teams(request):
	if request.method == 'POST':
		return doAddTeam(request)
	
	cschallenge_data = context_processors.cschallenge(request)
	if cschallenge_data is None and cschallenge_data['csc_registration_is_on'] is False:
		messages.info(request, "Registration is closed")
		
	userTeams = Group.objects.filter(challenge=cschallenge_data['cschallenge'], coach=request.user)
	schools = School.objects.all()
	
	context = {
		'title': config.app + ' | Cargo Space Challenge Team', 
		'page': 'team',
		'schools': schools,
		'teams': userTeams,
	}
	return render_template(context, request, template_name = "team")

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
		

def doAddTeam(request):
	print("hello gorillas")
	cschallenge_data = context_processors.cschallenge(request)
	if cschallenge_data is None and cschallenge_data['csc_registration_is_on'] is False:
		messages.info(request, "Registration is closed")
		print("hello")
		return redirect(teams)
	team_form = GroupForm(data=request.POST)
	if team_form.is_valid():
		team_form.save(commit=False)
		team_form.coach = request.user
		team_form.challenge = cschallenge_data['cschallenge']
		if request.user.is_superuser:
			team_form.verified = True
		team_form.save()
		messages.info(request, "Succesfuly create the team")
		return redirect(teams)
	else:
		print("we here gorillas")
		messages.info(request, messages.ERROR, "Please check the inputs and try again")
		return redirect(teams)


def doAddMember(request):
	cschallenge_data = context_processors.cschallenge(request)
	if cschallenge_data is None and cschallenge_data['csc_registration_is_on'] is False:
		messages.info(request, "Registration is closed")
		return redirect(teams)
	member_form = MemberForm(data=request.POST)
	if member_form.is_valid():
		member_form.save(commit=False)
		member_form.coach = request.user
		member_form.challenge = cschallenge_data['cschallenge']
		if request.user.is_superuser:
			member_form.verified = True
		member_form.save()
		return redirect(teams)
	else:
		messages.info(request, messages.ERROR, "Please check the inputs and try again")
		return redirect(teams)