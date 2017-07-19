from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /sign-in/
    url(r'^sign-in/$', views.sign_in, name='sign-in'),
]
