from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /sign-in/
    url(r'^sign-in/$', views.InscriptionWizard.as_view(), name='sign-in'),
    url(r'^sign-in/(?P<id>[0-9]+)/(?P<key>[0-9a-f]{40})/$', views.sign_in_validation,
        name='sign-in-validation'),
]
