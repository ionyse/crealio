# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$', 'portfolio.administration.views.profil'),
                       (r'^accueil/$', 'portfolio.administration.views.modifAccueilContact', {'page_slug': 'accueil'}),
                       (r'^contact/$', 'portfolio.administration.views.modifAccueilContact', {'page_slug': 'contact'}),
                       (r'^cv/page/$', 'portfolio.administration.views.modifCvPortfolio', {'page_slug': 'cv'}),
                       (r'^cv/infos/$', 'portfolio.cv.views.admin',),
                       (r'^cv/apparence/$', 'portfolio.cv.views.organisation',),
                       (r'^crealio/page/$', 'portfolio.administration.views.modifCvPortfolio', {'page_slug': 'crealio'}),
                       (r'^crealio/projets/$', 'portfolio.creabook.views.liste'),
                       (r'^crealio/projets/new/$', 'portfolio.creabook.views.new'),
                       (r'^crealio/projets/(?P<id>\d+)/$', 'portfolio.creabook.views.edit'),
                       (r'^informations/$', 'portfolio.administration.views.modifInformation'),
                       (r'^apparence/$', 'portfolio.administration.views.apparence'),
                       (r'^password/$', 'portfolio.administration.views.changePassword'),
                       (r'^stats/$', 'portfolio.statistic.views.pages'),
                       (r'^identite/$', 'portfolio.administration.views.changeIdentite'),
                       (r'^identite/supprimer/$', 'portfolio.administration.views.supprIdentite'),
                       (r'^email/$', 'portfolio.administration.views.changeMail'),
                       (r'^email/valide/(?P<id>\d+)/(?P<clef>\w{40})/$', 'portfolio.administration.views.valide'),
                       (r'^changePageStatus/(?P<page_slug>\w+)/$', 'portfolio.administration.views.onOffPage'),
                       (r'^suggestion/$', 'portfolio.administration.views.suggestion'),
                       (r'^delete/$', 'portfolio.administration.views.delete'),
)
