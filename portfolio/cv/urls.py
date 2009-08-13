# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'portfolio.cv.views.cv'),  # Affichage du book
)
