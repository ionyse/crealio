# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

class Field(models.Model):
    title = models.CharField('titre', max_length=80)
    slug  = models.CharField('slug', max_length=32)
    order = models.IntegerField('ordre')
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return u'%s' % (self.title)

class Item(models.Model):
    title = models.CharField('titre', max_length=32)
    slug  = models.CharField('slug', max_length=12)
    desc  = models.TextField('description')
    field = models.ForeignKey(Field)
    order = models.IntegerField('ordre')

    def __unicode__(self):
        return u'%s > %s' % (self.field.title, self.title)

