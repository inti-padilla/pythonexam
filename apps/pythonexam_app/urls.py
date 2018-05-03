from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout', views.logout),
    url(r'^view_user/(?P<id>\d+)$', views.view_user),
    url(r'^add_friend/(?P<id>\d+)$', views.add_friend),
    url(r'^del_friend/(?P<id>\d+)$', views.del_friend),
]