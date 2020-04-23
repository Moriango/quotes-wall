from django.conf.urls import url
from .import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^logout$', views.logout),
    url(r'^register_val$', views.register_val),
    url(r'^register$', views.register),
    url(r'^home_login$', views.home_login),
    url(r'^login$', views.home),
    url(r'^create$', views.create),
    url(r'^show/(?P<id>\d+)$', views.show),
    url(r'^destroy/(?P<id>\d+)$', views.delete),
    url(r'^likes/(?P<id>\d+)$', views.likes),
    url(r'^edit/$', views.edit),
    url(r'^create_edit/$', views.create_edit),
]