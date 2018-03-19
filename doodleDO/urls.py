from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<meeting_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<meeting_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<meeting_id>[0-9]+)/choose_room/$', views.choose_room, name='choose_room'),
]