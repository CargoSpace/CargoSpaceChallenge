from django import forms

from contest.models import ContestSubmission, ProblemSet, ProblemInput

class ContestSubmissionForm(forms.ModelForm):
	class Meta:
		model = ContestSubmission
		exclude = ["submitted_by","accepted"]
		fields = [
			"contest",
			"problem",
			"submission",#forms.FileField()
		]
		

class ProblemSetForm(forms.ModelForm):
	class Meta:
		model = ProblemSet
		exclude = ["created_by","problem_color", "language", 
			"problem_stdin", "problem_stdin"]
		fields = [
			"problem_type",
			"title",
			"source_credit",
			"description",
			"example_input",#forms.FileField()
			"example_output",#forms.FileField()
			"problem_type",
		]

class ProblemInputForm(forms.ModelForm):
	class Meta:
		model = ProblemInput
		exclude = ["problem","label","language", 
			"problem_type",
			"title",
			"source_credit",
			"description",
			"example_input",
			"example_output",
			"problem_type",]
		fields = [
			"problem_stdin",#forms.FileField()
			"problem_stdout",#forms.FileField()
		]