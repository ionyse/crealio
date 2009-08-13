# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<page_slug>[A-Za-z0-9_-]+)/$', 'portfolio.pages.views.page'),  # Affichage d'une page
)
