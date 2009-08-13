# -*- coding: utf-8 -*-

from portfolio.cv.models import Field, Item
from django import forms

class FieldForm(forms.ModelForm):
    class Meta:
        model   = Field
        fields  = ('title')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('title', 'desc')
