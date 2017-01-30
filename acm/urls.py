from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'schools', views.schools),
    url(r'teams$', views.teams),
    url(r'teams/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.team_details),
]