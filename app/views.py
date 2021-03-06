import inspect
import config #import configuration file ./config.py
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm

import time
from datetime import datetime, date
from contest.models import Contest, ContestSetting
import requests
from contest.forms import ContestSubmissionForm
from contest import lib
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from contest import tasks as contestTasks
import shelve

# Function to render templates
def render_template(context, request, template_name = "default"):
	page_name = template_name
	if template_name == "default":
		template_name = page_name = inspect.stack()[1][3] #Use calling function's name if temp is not set or is deault
	template_name = "app/" + template_name + ".html"
	template_obj = loader.get_template(template_name)
	return HttpResponse(template_obj.render(context, request))

def index(request):
	contest = Contest.objects.filter(contest_type="Regular", start_time__lt=timezone.now(), end_time__gt=timezone.now()).first() #ascending order
	contestIsActive = True if contest else False
	nextContest = getNextContest(contestIsActive)
	context = {
		'title': 'Exercise Daily and Become an Efficient Software Engineer | ' + config.app, 
		'page': 'home',
		'countDown': {
			'now': str(datetime.utcnow())[:19],
			'end_time': nextContest['start_time'][:19] if nextContest else str(datetime.utcnow())[:19],
			'tDifInMil': 0
		},
		'activeCountDown': {
			'now': str(datetime.now())[:19] if contestIsActive else str(datetime.now())[:19],
			'end_time': str(contest.end_time)[:19] if contestIsActive else str(datetime.now())[:19],
			'tDifInMil': 0
		},
		'contestIsActive': contestIsActive,
		'current_contest': contest
	}
	return render_template(context, request)

def getNextContest(contestIsActive):
	response = None
	if False:
		response = requests.get("https://csc-contest-maker.herokuapp.com/next_contest")
		if response.status_code != 200:
			return None
		response = response.json()
		return response
	else:
		Cache = shelve.open("AppSettings", flag='r')
		if "next_contest" in Cache:
			response = {'start_time':  Cache['next_contest']}
		Cache.close()
	return response
	
@login_required(login_url='/login')
def running_contest(request):
	
	contest = Contest.objects.filter(contest_type="Regular", start_time__lt=timezone.now(), end_time__gt=timezone.now()).first() #ascending order
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
	
	nextContest = getNextContest(contestIsActive)
	context = {
		'title': 'Contest is Running | ' + config.app if contestIsActive else 'Play time is over | ' + config.app, 
		'page' : 'running_contest',
		'contestIsActive': contestIsActive,
		'contest': contest,
		'contestProblems': contestProblems,
		'currentProblem' : currentProblem,
		'currentProblemInputs': currentProblemInputs,
		'countDown': {
			'now': str(datetime.utcnow())[:19],
			'end_time': nextContest['start_time'][:19] if nextContest else str(datetime.utcnow())[:19],
		},
		'activeCountDown': {
			'now': str(datetime.now())[:19] if contestIsActive else str(datetime.now())[:19],
			'end_time': str(contest.end_time)[:19] if contestIsActive else str(datetime.now())[:19],
		},
	}
	return render_template(context, request, 'running_contest')

def all_submissions(request):
	
# 	contest = Contest.objects.filter(start_time__lt=timezone.now(), end_time__gt=timezone.now()).first() #ascending order
# 	contestIsActive = True if contest else False
	contestIsActive = False
	if not contestIsActive:
		contest = Contest.objects.filter(contest_type="Regular").order_by('-created_at').first() #ascending order
		contestIsActive = True if contest.start_time <= timezone.now() and contest.end_time >= timezone.now() else False
	contestProblems = contest.contest_problems.all() if contest else None
	nextContest = getNextContest(contestIsActive)
	context = {
		'title': 'Contest is Running | ' + config.app if contestIsActive else 'Play time is over | ' + config.app, 
		'page' : 'running_contest',
		'contestIsActive': contestIsActive,
		'contest': contest,
		'contestProblems': contestProblems,
		'pastContests': Contest.objects.all().order_by('-created_at')[:64], # past 1 week
		'countDown': {
			'now': str(datetime.utcnow())[:19],
			'end_time': nextContest['start_time'][:19] if nextContest else str(datetime.utcnow())[:19],
		},
		'activeCountDown': {
			'now': str(datetime.now())[:19] if contestIsActive else str(datetime.now())[:19],
			'end_time': str(contest.end_time)[:19] if contestIsActive else str(datetime.now())[:19],
		},
	}
	return render_template(context, request, 'all_submissions')
def submission_details(request, pk):
	contest = Contest.objects.get(pk=pk)
	contestIsActive = True if contest.start_time <= timezone.now() and contest.end_time >= timezone.now() else False
	contestProblems = contest.contest_problems.all() if contest else None
	nextContest = getNextContest(contestIsActive)
	context = {
		'title': 'Contest is Running | ' + config.app if contestIsActive else 'Play time is over | ' + config.app, 
		'page' : 'running_contest',
		'contestIsActive': contestIsActive,
		'contest': contest,
		'contestProblems': contestProblems,
		'pastContests': Contest.objects.all().order_by('-created_at')[:64], # past 1 week 8 Contest per day 7 days
		'countDown': {
			'now': str(datetime.utcnow())[:19],
			'end_time': nextContest['start_time'][:19] if nextContest else str(datetime.utcnow())[:19],
		},
		'activeCountDown': {
			'now': str(datetime.now())[:19],
			'end_time': str(contest.end_time)[:19] if contestIsActive else str(datetime.now())[:19],
		},
	}
	return render_template(context, request, 'all_submissions')

@login_required(login_url='/login')
def custom_contest(request, pk):
	try:
		contest = Contest.objects.get(pk=pk)
		contestIsActive = False
		contestIsValid = False
		if contest.start_time < timezone.now() and contest.end_time > timezone.now():
			contestIsActive = True
		if contest.start_time > timezone.now():
			contestIsValid = True
			
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
			'title': 'Contest is Running | ' + config.app if contestIsActive else 'Contest is over | ' + config.app, 
			'page' : 'running_contest',
			'contestIsActive': contestIsActive,
			'contestIsValid': contestIsValid,
			'contest': contest,
			'contestProblems': contestProblems,
			'currentProblem' : currentProblem,
			'currentProblemInputs': currentProblemInputs,
			'countDown': {
				'now': str(datetime.utcnow())[:19],
				'end_time': str(contest.start_time)[:19] if contestIsValid else str(datetime.utcnow())[:19],
			},
			'activeCountDown': {
				'now': str(datetime.now())[:19] if contestIsActive else str(datetime.now())[:19],
				'end_time': str(contest.end_time)[:19] if contestIsActive else str(datetime.now())[:19],
			},
		}
		return render_template(context, request, 'running_custom_contest')
	except Contest.DoesNotExist:
		messages.info(request, "Contest doesn't exist")
		return redirect(index)
	
@login_required(login_url='/login')
def doSubmission(request):
	if request.method == 'POST':
		form = ContestSubmissionForm(request.POST, request.FILES)
		if form.is_valid():
			#Check if contest exists and that contest is still running
			try:
				aContest = Contest.objects.get(pk=request.POST['contest'])
			except Contest.DoesNotExist:
				messages.info(request, "Contest is over.")
				# return redirect(running_contest)
				return redirect(request.POST.get('next', '/'));
			bContest = Contest.objects.filter(start_time__lt=timezone.now(), end_time__gt=timezone.now()).first() #ascending order
			if bContest is None:
				messages.info(request, "Contest is over.")
				# return redirect(running_contest)
				return redirect(request.POST.get('next', '/'));
				
			contestSubmission = form.save(commit=False)
			workerStatus = lib.get_celery_worker_status()
			contestSubmission.submitted_by = request.user
			contestSubmission.save()
			
			if 'ERROR' in workerStatus:
				# Worker not running, judge now now
				contestTasks.judge_submission(contestSubmission.pk)
			else:
				contestTasks.judge_submission.delay(contestSubmission.pk)
			messages.info(request, "Successfuly Submitted")
			# return redirect(running_contest)
			return redirect(request.POST.get('next', '/'));
		else:
			messages.info(request, "Sorry, Please check your input and try again.")
			# return redirect(running_contest)
			return redirect(request.POST.get('next', '/'));
	# return redirect(running_contest)
	return redirect(request.POST.get('next', '/'));
	
def doAuth(request):
	if request.method == 'POST':
		redirect_to = request.POST['next'] if 'next' in request.POST else running_contest
		if request.POST['username'] and request.POST['password']:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				if user.is_superuser:
					return redirect(redirect_to)
				else:
					return redirect(redirect_to)
			else:
				messages.info(request, "Please check the inputs and try again")
				return redirect(auth)
	return redirect(auth)

def doRegister(request):
	if request.method == 'POST':
		redirect_to = request.POST['next'] if 'next' in request.POST else running_contest
		register_form = RegisterForm(data=request.POST)
		if register_form.is_valid():
			username = request.POST['username']
			display_name = request.POST['display_name']
			email = request.POST['email']
			password = request.POST['password']
			user = User.objects.create_user(username=username, email=email, password=password)
			if user is not None:
				user.first_name = display_name
				user.save()
				user = authenticate(username=username, password=password)
				login(request, user)
				if user:
					if user.is_superuser:
						return redirect(redirect_to) # redirect to our dashboard
					else:
						return redirect(redirect_to)
				else:
					return redirect(register)
			else:
				messages.info(request, "Please check the inputs and try again")
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
	context = { 'title': 'Login | ' + config.app, 
	'page' : 'login',
	'redirect_to':  request.GET['next'] if 'next' in request.GET else False
	}
	return render_template(context, request, 'login')
	
# /register
def register(request):
	if request.method == 'POST':
		return doRegister(request)
	context = { 'title': 'Register | ' + config.app, 
	'page' : 'register', 
	'redirect_to': request.GET['next'] if 'next' in request.GET else False
	}
	return render_template(context, request, 'register')
	
# /forgot_password
def forgot_password(request):
	context = { 'title': 'Forgot Password | ' + config.app, 'page' : 'forgot_password' }
	return render_template(context, request, 'forgot_password')