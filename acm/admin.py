from django.contrib import admin
from .models import Challenge, School, Group, Member
# Register your models here.

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'start_time', 'end_time', 'registration_close_at',)
	search_fields = ('title', 'description', )


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_at', 'verified',)
	search_fields = ('title', )
	
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	list_display = ('team_name', 'school', 'challenge', 'coach', 'created_at', 'verified',)
	search_fields = ('team_name', 'school', 'challenge', )

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
	list_display = ('group', 'member', 'verified',)
	search_fields = ('group', 'member', 'challenge', )