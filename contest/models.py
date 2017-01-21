from __future__ import unicode_literals
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from crum import get_current_user
# Create your models here.

class ProblemSet(models.Model):
	"""ProblemSet Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.TextField(default=None)
	description = models.TextField()
	language = models.CharField(max_length=5, default='en')
	image = models.FileField(null=True, blank=True)
	problem_type = models.CharField(max_length=30, choices=(
		('A', 'Problem A'), 	#Simplest
		('B', 'Problem B'), 	#Simpler
		('C', 'Problem C'), 	#Simple
		('D', 'Problem D') ) )	#Hard
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, default=None)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.title)
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and not user.pk:
			user = None
		if not self.pk:
			self.created_by = user
		super(ProblemSet, self).save(*args, **kwargs)
		

class ProblemInput(models.Model):
	"""ProblemInput Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	label = models.TextField()
	problem = models.ForeignKey(ProblemSet, on_delete=models.CASCADE)
	language = models.CharField(max_length=5, default='en')
	problem_stdin = models.FileField(null=False, blank=False)
	problem_stdout = models.FileField(null=False, blank=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.label)

class Contest(models.Model):
	"""ProblemInput Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.TextField()
	description = models.TextField(null=True, blank=True)
	image = models.FileField(null=True, blank=True)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	language = models.CharField(max_length=5, default='en')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.title)
		
class ContestProblem(models.Model):
	"""ContestProblem Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	contest = models.ForeignKey(Contest, related_name='contest_problems', on_delete=models.CASCADE)
	problem = models.ForeignKey(ProblemSet, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.contest)
		

class ContestSubmission(models.Model):
	"""ContestSubmission Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
	problem = models.ForeignKey(ProblemSet, on_delete=models.CASCADE)
	submission = models.FileField(null=False, blank=False)
	submitted_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, default=None)
	accepted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.contest)
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and not user.pk:
			user = None
		if not self.pk:
			self.submitted_by = user
		super(ContestSubmission, self).save(*args, **kwargs)
		
class AutoContestTitle(models.Model):
	"""ContestTitle Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.TextField(blank=False, null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.title)


class ContestSetting(models.Model):
	"""ContestSetting Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.TextField(default="Settings")
	interval = models.IntegerField(default=3) #Hours
	duration = models.IntegerField(default=30) #Minutes
	pauseAutomaticContest = models.BooleanField(default=False)
	useAutoContestTitle = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.title)