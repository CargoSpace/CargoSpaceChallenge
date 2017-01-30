from django import forms

from .models import School, Group, Member

class SchoolForm(forms.ModelForm):
	class Meta:
		model = School
		exclude = ("verified",)
		fields = (
			"title",
		)

class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		excludes = ['challenge','coach','verified',]
		fields = ('team_name', 'school',)

class MemberForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = (
			"member",
			"group",
		)