import config
from django.conf import settings

def extra_context(request):
    return {
      'app_name':  config.app,
      'user': request.user
    }
    
def debug(context):
  return {'DEBUG': settings.DEBUG}