from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
	url(r'^add/(?P<period>[A-Z]+[0-9]+)/(?P<sample>[0-9]+)/(?P<threshold>[0-9\.]+)$', 
		views.add),
	url(r'^delete/(?P<period>[A-Z]+[0-9]+)/(?P<sample>[0-9]+)/(?P<threshold>[0-9\.]+)$', 
		views.delete),
	url(r'^checkin$', views.checkin)
)
