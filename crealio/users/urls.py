from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /sign-in/
    url(r'^sign-in/$', views.index, name='index'),
]
