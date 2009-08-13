# -*- coding: utf-8 -*-

from portfolio.pages.models import Page
from portfolio.commercial.models import Profile

from django import forms

class PageForm(forms.ModelForm):
    onglet = forms.BooleanField('Onglet ?')
    
    class Meta:
        model   = Page
        fields  = ('title', 'intro', 'content', 'actif')
