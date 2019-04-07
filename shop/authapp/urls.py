from django.conf.urls import url
from . import views

app_name = 'authapp'

urlpatterns = [
    url('^login$', views.login, name='login'),
    url('^logout$', views.logout, name='logout'),
    url('^register', views.register, name='register'),
    url('^edit', views.edit, name='edit'),
    url('^view', views.view, name='view')
]
