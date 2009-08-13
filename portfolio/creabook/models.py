# -*- coding: utf-8; -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

class BookEntry(models.Model):
    title = models.CharField('titre', max_length=80)
    slug = models.CharField('slug', max_length=32)
    date = models.DateField('date de réalisation')
    desc = models.TextField('description')
    image = models.ImageField('image', upload_to='book/images/%Y/%m/%d', blank=True, null=True)
    file = models.FileField('fichier joint (SWF, ZIP, Code Source, PSD)', upload_to='book/files/%Y/%m/%d', blank=True, null=True)
    force_download = models.BooleanField('Forcer le téléchargement du fichier joint')
    url = models.URLField('Lien', blank=True)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = "Book Entry"
        verbose_name_plural = "Book Entries"

    def is_long(self):
        return (len(self.desc) >= 800)

    def __unicode__(self):
        return u'%s' % (self.title)
