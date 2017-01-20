from django import forms

from contest.models import ContestSubmission

class ContestSubmissionForm(forms.ModelForm):
	class Meta:
		model = ContestSubmission
		exclude = ["submitted_by","accepted"]
		fields = [
			"contest",
			"problem",
			"submission",#forms.FileField()
		]