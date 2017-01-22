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
	problem_color = models.TextField(null=True, blank=True, default='Blue') #ACM style naming
	source_credit = models.TextField(default=None)
	description = models.TextField()
	language = models.CharField(max_length=5, default='en')
	image = models.FileField(null=True, blank=True)
	example_input = models.TextField(null=True, blank=True)
	example_output = models.TextField(null=True, blank=True)
	problem_type = models.CharField(max_length=30, choices=(
		('A', 'Problem A'),
		('B', 'Problem B'),
		('C', 'Problem C'),
		('D', 'Problem D') ), default='A' ) # Codeforces problem tagging from Easiest (A) to hardest (D)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.title)
		

class ProblemInput(models.Model):
	"""ProblemInput Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	label = models.TextField()
	problem = models.ForeignKey(ProblemSet, related_name='problem_input', on_delete=models.CASCADE)
	language = models.CharField(max_length=5, default='en')
	point = models.IntegerField(default=10)
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
	contest_type = models.CharField(max_length=20, choices=(
		('Regular', 'Regular'),
		('ACM-Style', 'ACM-Style'),
		('Code-Jam-Style', 'Code-Jam-Style')), default='Regular' )
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
	submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
	submission_state = models.CharField(max_length=20, choices=(
		('Pending', 'Pending'),
		('Accepted', 'Accepted'),
		('Rejected', 'Rejected')), default='Pending' )
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.contest)
		
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
	last_read_next_contest = models.TextField(blank=True, null=True)
	pauseAutomaticContest = models.BooleanField(default=False)
	useAutoContestTitle = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.title)