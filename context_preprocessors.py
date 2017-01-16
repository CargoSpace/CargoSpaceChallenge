import config
def extra_context(request):
    return { 'app_name':  config.app}