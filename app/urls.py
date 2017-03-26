from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^index', views.index, name='homepage'),
    url(r'^contest$', views.running_contest, name='running_contest'),
    url(r'^submission$', views.doSubmission),
    url(r'^submissions$', views.all_submissions),
    url(r'submissions/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.submission_details),
    
    # Custom Contest (views.custom_submission_details)
    # url(r'^contests', views.custom_contests),
    url(r'contest/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.custom_contest),
    
    url(r'^login', views.auth),
    url(r'^register', views.register),
    
    url(r'^logout', views.logout_user),
    url(r'^forgot_password', views.forgot_password),
]