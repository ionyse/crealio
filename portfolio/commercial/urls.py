# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from portfolio.commercial.forms import Step1, Step2, InscriptionWizard, contactForm

urlpatterns = patterns('',
    (r'^$', 'portfolio.commercial.views.inscription'),
    (r'^formulaire/$', InscriptionWizard([Step1, Step2])),
    (r'^valide/(?P<id>\d+)/(?P<clef>\w{40})/$', 'portfolio.commercial.views.valide'),
    (r'^contact/$', 'portfolio.commercial.views.contact'),
)
