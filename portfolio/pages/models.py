# -*- coding: utf-8; -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class Page(models.Model):
    title = models.CharField('titre', max_length=80)
    slug = models.CharField('slug', max_length=32)
    onglet = models.IntegerField('ordre (0 pour pas d\'onglet)',null=True)
    pub_date = models.DateTimeField('date de modification',auto_now=True)
    intro = models.TextField('introduction', blank=True)
    content = models.TextField('contenu', blank=True)
    actif = models.BooleanField('En ligne')
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return u'%s > %s' % (self.user, 
                             self.title)
