import inspect
import config #import configuration file ./config.py
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm

import time
from datetime import datetime, date
from contest.models import Contest
from rpc import rpc_methods
import requests
from contest.forms import ContestSubmissionForm
from . import lib
from django.contrib.auth.decorators import login_required

# Function to render templates
def render_template(context, request, template_name = "default"):
	page_name = template_name
	if template_name == "default":
		template_name = page_name = inspect.stack()[1][3] #Use calling function's name if temp is not set or is deault
	template_name = "app/" + template_name + ".html"
	template_obj = loader.get_template(template_name)
	return HttpResponse(template_obj.render(context, request))

def index(request):
	contest = Contest.objects.filter(start_time__gt=datetime.now()).order_by('-start_time').first() #ascending order
	response = requests.get("https://csc-contest-maker.herokuapp.com/next_contest")
	if response.status_code != 200:
		return
	sReponse = response.json()
	context = {
		'title': config.app + ' | Algorithm Warm-up Everyday at 12PM', 
		'page': 'home',
		'countDown': {
			'now': str(datetime.utcnow()),
			'end_time': sReponse['start_time'],
		},
		'contestIsRunning': False,
		'current_contest': None
	}
	return render_template(context, request)
	
@login_required(login_url='/login')
def running_contest(request):
	
	contest = Contest.objects.filter(start_time__lt=datetime.now(), end_time__gt=datetime.now()).first() #ascending order
	contestIsActive = True if contest else False
	contestProblems = contest.contest_problems.all() if contest else None
	problemType = request.GET.get("type", "A")
	currentProblem = contestProblems[0].problem if contest else None
	currentProblemInputs = None
	if currentProblem:
		for contestProblem in contestProblems:
			if contestProblem.problem.problem_type == problemType:
				currentProblem = contestProblem.problem
				currentProblemInputs = contestProblem.problem.problem_input.all()
				break
	context = {
		'title': 'Contest is Running | ' + config.app, 
		'page' : 'running_contest',
		'contestIsActive': contestIsActive,
		'contest': contest,
		'contestProblems': contestProblems,
		'currentProblem' : currentProblem,
		'currentProblemInputs': currentProblemInputs,
		'countDown': {
			'now': str(datetime.now()) if contestIsActive else str(datetime.now()),
			'end_time': str(contest.end_time) if contestIsActive else str(datetime.now()),
		},
	}
	return render_template(context, request, 'running_contest')

@login_required(login_url='/login')
def doSubmission(request):
	if request.method == 'POST':
		form = ContestSubmissionForm(request.POST, request.FILES)
		if form.is_valid():
			#TODO: Perform comparison here
			submission = form.save(commit=False)
			submission.submitted_by = request.user
			submission.save()
			messages.success(request, "Successfuly Submitted");
			return redirect(running_contest)
		else:
			messages.error(request, "Sorry, Please check your input and try again.")
			return redirect(running_contest)
	return redirect(running_contest);
	
def doAuth(request):
	if request.method == 'POST':
		if request.POST['username'] and request.POST['password']:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				if user.is_superuser:
					return redirect(running_contest)
				else:
					return redirect(running_contest)
			else:
				messages.error(request, "Please check the inputs and try again")
				return redirect(auth)
	return redirect(auth)

def doRegister(request):
	if request.method == 'POST':
		print(request.POST)
		if request.POST['mobile'] and request.POST['email'] and request.POST['password'] and request.POST['full_name']:
			username = request.POST['mobile']
			full_name = request.POST['full_name']
			email = request.POST['email']
			password = request.POST['password']
			user = User.objects.create_user(username=username, email=email, password=password)
			if user is not None:
				user = authenticate(username=username, password=password)
				login(request, user)
				if user.authenticated:
					if user.is_superuser:
						return redirect(running_contest) # redirect to our dashboard
					else:
						return redirect(running_contest)
				else:
					return redirect(register)
			else:
				messages.error(request, "Please check the inputs and try again")
				return redirect(register)
	else:
		return redirect(register)
	

def logout_user(request):
	logout(request)
	return redirect(auth)
	
# login
def auth(request):
	if request.method == 'POST':
		return doAuth(request)
	context = { 'title': 'Login | ' + config.app, 'page' : 'login' }
	return render_template(context, request, 'login')
	
# /register
def register(request):
	if request.method == 'POST':
		return doRegister(request)
	context = { 'title': 'Register | ' + config.app, 'page' : 'register' }
	return render_template(context, request, 'register')
	
# /forgot_password
def forgot_password(request):
	context = { 'title': 'Forgot Password | ' + config.app, 'page' : 'forgot_password' }
	return render_template(context, request, 'forgot_password')