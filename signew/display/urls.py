from django.conf.urls import url
from . import views

app_name = 'display'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<display_id>[0-9]+)/$', views.show, name='show'),
]
