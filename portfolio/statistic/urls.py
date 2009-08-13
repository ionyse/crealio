# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^pages/$', 'portfolio.pages.views.page'),  # Affichage des pages
)
