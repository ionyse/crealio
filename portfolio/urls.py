# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from portfolio.settings import MEDIA_ROOT

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Une view qui va rediriger vers la page d'accueil du site
                       (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/accueil/'}),

                       # URL des medias #
                       (r'^medias/(?P<path>.*)$',
                        'django.views.static.serve',
                        {'document_root': MEDIA_ROOT}),
                       (r'^jsi18n/$', 'django.views.i18n.javascript_catalog',
                        {'packages': 'django.conf'}),

                       
                       # Site commercial
                       (r'^inscription/', include('portfolio.commercial.urls')),
                       (r'^connexion/', 'django.views.generic.simple.redirect_to', {'url': '/accounts/login/'}),
                       (r'^rechercher/', 'portfolio.commercial.views.rechercher'),
                       (r'^annuaire/', 'portfolio.commercial.views.annuaire'),
                       (r'^presentation/', 'portfolio.commercial.views.presentation'),
                       (r'^tutoriels/', 'portfolio.commercial.views.tutoriels'),
                       (r'^plan/', 'portfolio.commercial.views.plan'),
                       (r'^partenaires/', 'portfolio.commercial.views.partenaires'),

                       # Administration commercial
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/(.*)', admin.site.root),

                       # Site de l'utilisateur
                       #(r'^accueil/$', 'portfolio.pages.views.page', {'page_slug': 'accueil'}),
                       (r'^administration/', include('portfolio.administration.urls')),
                       (r'^crealio/', include('portfolio.creabook.urls')),  # Affichage d'un portfolio
                       (r'^cv/', include('portfolio.cv.urls')),  # Affichage du CV

                       # Les deux
                       (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'commercial/login.html'}),
                       (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'commercial/logout.html'}),
                       (r'^contact/$', 'portfolio.commercial.views.contact'),
                       
                       (r'^favicon.ico$', 'django.views.generic.simple.redirect_to', {'url': '/medias/favicon.ico'}),
                       
                       (r'^', include('portfolio.pages.urls')),  # Affichage d'une page par défault
)
