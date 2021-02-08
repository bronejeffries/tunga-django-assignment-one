from django.conf.urls import url
from . import views

app_name = 'vistors'

urlpatterns = [
    url(r'^create/$', views.register_entry, name='create'),
    url(r'^search/$', views.search_entry, name='search'),
    url(r'^search/add/$', views.search_to_add, name='search_to_add'),

]