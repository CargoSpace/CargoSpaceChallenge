from django.contrib import admin

# Register your models here.
from .models import ProblemSet, ProblemInput, Contest, ContestProblem, ContestSubmission

@admin.register(ProblemSet)
class ProblemSetAdmin(admin.ModelAdmin):
	list_display = ('problem', 'created_by', 'language', 'problem_type', 'created_at',)
	search_fields = ('problem', 'problem_type', )
	
	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_by = request.user
			obj.save()

@admin.register(ProblemInput)
class ProblemInputAdmin(admin.ModelAdmin):
	list_display = ('label', 'problem', 'language', 'created_at',)
	search_fields = ('label', 'problem', )

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'language', 'start_time', 'end_time', 'created_at',)
	search_fields = ('title', 'description', )
	

@admin.register(ContestProblem)
class ContestProblemAdmin(admin.ModelAdmin):
	list_display = ('contest', 'problem', 'created_at',)
	search_fields = ('contest', )

@admin.register(ContestSubmission)
class ContestSubmissionAdmin(admin.ModelAdmin):
	list_display = ('contest', 'problem', 'submitted_by', 'created_at',)
	search_fields = ('contest', 'submitted_by',)
	def save_model(self, request, obj, form, change):
		if not change:
			obj.submitted_by = request.user
			obj.save()