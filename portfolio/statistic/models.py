# -*- coding:utf-8 -*-
from django.db import models

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class Statistics(models.Model):
    ip = models.IPAddressField('IP')
    query = models.TextField('Page demandée',null=True)
    date = models.DateTimeField('date de connexion',auto_now=True)
    user_agent = models.ForeignKey('UserAgent')
    site = models.ForeignKey(Site)

    def plus_vus():
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT d.id, COUNT(*) as sum
            FROM statistic_statistics s
            LEFT JOIN django_site d ON s.site_id = d.id
            WHERE d.id <> 1
            GROUP BY d.id
            ORDER BY sum DESC
            LIMIT 6""")
        result_list = []
        for row in cursor.fetchall():
            s = Site.objects.get(pk=row[0])
            result_list.append(s)
        print result_list
        return result_list


    plus_vus = staticmethod(plus_vus)

    def __unicode__(self):
        return u'%s > %s > %s' % (self.date, self.ip, self.query)

    class Meta:
        verbose_name_plural = "Statistics"

class UserAgent(models.Model):
    os = models.ForeignKey('OS', null=True)
    browser = models.ForeignKey('Browser', null=True)
    agent = models.TextField('User Agent')

    def __unicode__(self):
        return u'%s' % self.agent

class OS(models.Model):
    name = models.CharField('name', max_length=25)
    version = models.CharField('version', max_length=10)

    class Meta:
        verbose_name = "Operating System"
        verbose_name_plural = "Operating Systems"

    def __unicode__(self):
        return u'%s %s' % (self.name, self.version)

class Browser(models.Model):
    name = models.CharField('name', max_length=25)
    version = models.CharField('version', max_length=10)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.version)
