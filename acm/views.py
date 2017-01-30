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
from django.contrib.auth.models import User
from django.db.models import Q
from . import lib
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
	allTeams = Group.objects.filter(challenge=cschallenge_data['cschallenge'])
	schools = School.objects.all()
	
	context = {
		'title': config.app + ' | Cargo Space Challenge Team', 
		'page': 'team',
		'schools': schools,
		'userTeams': userTeams,
		'teams': allTeams,
	}
	return render_template(context, request, template_name = "team")

@login_required(login_url='/login')	
def team_details(request, pk):
	if request.method == 'POST':
		return doAddMember(request, pk)
	cschallenge_data = context_processors.cschallenge(request)
	if cschallenge_data is None and cschallenge_data['csc_registration_is_on'] is False:
		messages.info(request, "Registration is closed")
		return redirect(teams)
		
	try:
		team = Group.objects.get(pk=pk)
	finally:
		if team is None:
			return HttpResponse(status=404)
		
	members = Member.objects.filter(group=team)
	
	context = {
		'title': config.app + ' | Cargo Space Challenge Team', 
		'page': 'team-details',
		'team': team,
		'members': members,
	}
	return render_template(context, request, template_name = "team_details")
	
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
	cschallenge_data = context_processors.cschallenge(request)
	if cschallenge_data is None and cschallenge_data['csc_registration_is_on'] is False:
		messages.info(request, "Registration is closed")
		return redirect(teams)
	team_form = GroupForm(data=request.POST)
	if team_form.is_valid():
		team = team_form.save(commit=False)
		team.coach = request.user
		team.challenge = cschallenge_data['cschallenge']
		if request.user.is_superuser:
			team.verified = True
		team.save()
		messages.info(request, "Successful")
		return redirect(teams)
	else:
		messages.info(request, messages.ERROR, "Please check the inputs and try again")
		return redirect(teams)


def doAddMember(request, pk):
	cschallenge_data = context_processors.cschallenge(request)
	if cschallenge_data is None and cschallenge_data['csc_registration_is_on'] is False:
		messages.info(request, "Registration is closed")
		return redirect("/cschallenge/teams/" + pk)
	user = User.objects.filter(Q(username=request.POST['identity']) | Q(email=request.POST['identity']))
	if not user:
		print("usr not foundx")
		messages.info(request, "User not found! Has user registered?")
		return redirect("/cschallenge/teams/" + pk)
	member_form = MemberForm(data=request.POST)
	if member_form.is_valid():
		member = member_form.save(commit=False)
		member.member = user.first()
		if request.user.is_superuser:
			member.verified = True
		member.save()
		return redirect("/cschallenge/teams/" + pk)
	else:
		print("form not valid")
		print(member_form)
		messages.info(request, messages.ERROR, "Please check the inputs and try again")
		return redirect("/cschallenge/teams/" + pk)