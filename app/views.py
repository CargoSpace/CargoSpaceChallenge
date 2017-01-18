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
	rpc_methods.create_contest()
	print(contest.start_time)
	print(contest.end_time)
	
	context = { 
		'title': config.app + ' | Algorithm Warm-up Everyday at 12PM', 
		'page': 'home',
		'countDown': {
			'now': contest.start_time.strftime("%Y-%m-%d %H:%I:%S"),
			'end_time': contest.end_time.strftime("%Y-%m-%d %H:%I:%S"),
		},
		'contestIsRunning': False,
		'current_contest': None
	}
	return render_template(context, request)

def doAuth(request):
	if request.method == 'POST':
		form = LoginForm(request.POST or None)
		if form.is_valid():
			user = form.authenticate_via_email()
			if user is not None:
				login(request, user)
				if user.is_superuser:
					return redirect('/admin')
				else:
					return redirect(index)
		messages.error(request, "Please check the inputs and try again")
		return redirect(auth)
	else:
		return redirect('/login')

def doRegister(request):
	if request.method == 'POST':
		if request.POST['mobile'] and request.POST['email'] and request.POST['password'] and request.POST['name']:
			mobile = request.POST['mobile']
			name = request.POST['name']
			email = request.POST['email']
			password = request.POST['password']
			user = User.objects.create_user(username=mobile, email=email, password=password, full_name=name)
			if user is not None:
				login(request, user)
				if user.is_superuser:
					return redirect('/admin')
				else:
					return redirect(index)
			else:
				messages.error(request, "Please check the inputs and try again")
				return redirect(auth)
	else:
		return redirect('/register')
	

def logout_user(request):
    logout(request)
    return redirect(auth)
    
# login
def auth(request):
	context = { 'title': 'Login | ' + config.app, 'page' : 'login' }
	return render_template(context, request, 'login')
	
# /register
def register(request):
	context = { 'title': 'Register | ' + config.app, 'page' : 'register' }
	return render_template(context, request, 'register')
	
# /forgot_password
def forgot_password(request):
	context = { 'title': 'Forgot Password | ' + config.app, 'page' : 'forgot_password' }
	return render_template(context, request, 'forgot_password')