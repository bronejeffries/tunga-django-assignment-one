from django.conf.urls import url
from . import views

app_name = 'user_management'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^user/register/$', views.create_user, name="register")
]
