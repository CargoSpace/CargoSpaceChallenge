from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import config
import inspect
from contest.models import Contest, ContestSetting, ProblemSet
from contest.forms import ProblemSetForm, ProblemInputForm
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

# Function to render templates
def render_template(context, request, template_name = "default"):
	page_name = template_name
	if template_name == "default":
		template_name = page_name = inspect.stack()[1][3] #Use calling function's name if temp is not set or is deault
	template_name = "dashboard/" + template_name + ".html"
	template_obj = loader.get_template(template_name)
	return HttpResponse(template_obj.render(context, request))
	
def index(request):
	context = { 'title': config.app + ' | Cargo Space Challenge dashboard', 'page': 'dashboard' }
	return render_template(context, request)
	
	
def show_problems(request):
	problems = ProblemSet.objects.all()
	context = {
		'title': config.app + ' | Cargo Space Challenge Problemset', 
		'page': 'show-problems',
		'problems': problems,
	}
	return render_template(context, request, template_name = "problem/index")
	
def create_problem(request):
	if request.method == 'POST':
		problemSetForm = ProblemSetForm(request.POST, request.FILES)
		problemInputForm = ProblemInputForm(request.POST, request.FILES)
		if problemSetForm.is_valid() and problemInputForm.is_valid():
			problemSet = problemSetForm.save(commit=False)
			problemSet.created_by = request.user
			problemSet.save()
			problemInput = problemInputForm.save(commit=False)
			problemInput.problem = problemSet
			problemInput.save()
			messages.success(request, "Successfuly Submitted")
			return redirect(show_problems)
		else:
			print(problemSetForm)
			print(problemInputForm)
			messages.error(request, "Sorry, Please check your input and try again.")
			return redirect(create_problem)
	context = {'title': config.app + ' | Cargo Space Challenge Problemset', 'page': 'create-problem',}
	return render_template(context, request, template_name = "problem/create")