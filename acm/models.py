from __future__ import unicode_literals
from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Challenge(models.Model):
	"""Challenge Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.TextField()
	description = models.TextField(null=True, blank=True)
	image = models.FileField(null=True, blank=True)
	registration_close_at = models.DateTimeField()
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	language = models.CharField(max_length=5, default='en')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s %s' % (self.title, self.description)

class School(models.Model):
	"""School Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.TextField()
	verified = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.title)
		
class Group(models.Model):
	"""Group Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	team_name = models.TextField()
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
	coach = models.ForeignKey(User, on_delete=models.CASCADE)
	verified = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.team_name)

class Member(models.Model):
	"""Member Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	member = models.ForeignKey(User, on_delete=models.CASCADE)
	verified = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.member)