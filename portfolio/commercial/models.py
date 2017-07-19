# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class Pays(models.Model):
    code = models.CharField('code', max_length=2)
    name = models.CharField('nom', max_length=75)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name_plural = "Pays"

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site)

    # Added field
    address1 = models.CharField('adresse ligne 1', max_length=100, blank=True)
    address2 = models.CharField('adresse ligne 2', max_length=100, blank=True)
    zipcode = models.CharField('code postal', max_length=10, blank=True)
    city = models.CharField('ville', max_length=75)
    country = models.ForeignKey(Pays, related_name="Pays")

    dob = models.DateField('date de naissance', null=True, blank=True)
    pob = models.CharField('ville de naissance', max_length=75, blank=True)
    cob = models.ForeignKey(Pays, related_name="Pays de naissance", null=True, blank=True)

    nationality = models.CharField('nationnalité', max_length=75, blank=True)

    SEX = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )
    sex = models.CharField('sexe', choices=SEX, max_length=1, blank=True)

    d_licence = models.CharField('permis', max_length=100, blank=True)

    STATUS = (
        ('C', 'Célibataire'),
        ('M', 'Marié'),
        ('D', 'Divorcé'),
        ('P', 'Pacsé'),
        ('A', 'Autre'),
    )
    status = models.CharField('état civil', choices=STATUS,max_length=2, blank=True)
    phone = models.CharField('téléphone fixe', max_length=20, blank=True)
    mobile = models.CharField('portable', max_length=20, blank=True)
    metier = models.CharField('situation professionnelle', max_length=50)
    identite = models.ImageField('photo d\'identité', upload_to="identite", blank=True)

    def __unicode__(self):
        return u'%s' % (self.user)
