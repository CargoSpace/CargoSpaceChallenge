from .models import Challenge
from django.utils import timezone

def cschallenge(request):
	nextChallenge = Challenge.objects.filter(end_time__gt=timezone.now()).first() #ascending order
	registrationIsOn = False
	if nextChallenge:
		if nextChallenge.registration_close_at > timezone.now():
			registrationIsOn = True
	return {
	  'cschallenge':  nextChallenge,
	  'csc_registration_is_on':  registrationIsOn,
	}