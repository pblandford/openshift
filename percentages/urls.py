from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
	url(r'(?P<period>[A-Z]+[0-9]+)/(?P<sample>[0-9]+)$', views.receive),
	url(r'^upload$', views.upload),
)
