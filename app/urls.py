from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^index', views.index, name='homepage'),
    url(r'^contest', views.running_contest, name='running_contest'),
    url(r'^submission', views.doSubmission),
    
    url(r'^login', views.auth),
    url(r'^register', views.register),
    
    url(r'^logout', views.logout_user),
    url(r'^forgot_password', views.forgot_password),
]