from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'problem$', views.show_problems),
    url(r'problem/create', views.create_problem),
]