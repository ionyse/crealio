# -*- coding: utf-8 -*-

from portfolio.creabook.models import BookEntry
from django import forms

class BookEntryForm(forms.ModelForm):
    date = forms.DateField(label="Date de réalisation", input_formats=['%d/%m/%Y','%d-%m-%Y','%Y-%m-%d 00:00:00'], widget=forms.DateTimeInput(attrs={'class':'vDateField'}))

    class Meta:
        model   = BookEntry
        fields  = ('title', 'date', 'desc', 'image', 'file', 'force_download', 'url')

class signalerAbusForm(forms.Form):
    titleMail = forms.CharField(label='titleMail')
    textAbus = forms.CharField(label='textAbus',widget=forms.Textarea)

    def send(self, mails=[]):
        if self.is_valid():
            if not mails:
            	mails = [a[1] for a in ADMINS]
            # Codage de l'envoi
            subject = u'[%s] : %s' % (SITE_NAME,
                                      "Signalement d'un abus sur le site")
            msg = EmailMessage(subject, self.cleaned_data['textAbus'], 'no-reply@crealio.fr', mails)
            try:
                msg.send()
            except:
                print "Titre : %s\n\nMessage : %s\n" % (self.cleaned_data['titleMail'], self.cleaned_data['textAbus'])
                return False
            return True
        else:
            print self.errors
        return False


class recommanderForm(forms.Form):
    titleMail = forms.CharField(label='titleMail')
    mail = forms.EmailField(label='mail')
    textAbus = forms.CharField(label='textRecommander',widget=forms.Textarea)

    def send(self, mails=[]):
        if self.is_valid():
            if not mails:
                mails = [a[1] for a in ADMINS]
            # Codage de l'envoi
            subject = u'[%s] : %s' % (SITE_NAME,
                                       self.cleaned_data['titleMail'],)
            msg = EmailMessage(subject, self.cleaned_data['textRecommander'], 'no-reply@crealio.fr', self.cleaned_data['mail'])
            try:
                msg.send()
            except:
                print "Titre : %s\n\nMessage : %s\n" % (self.cleaned_data['titleMail'], self.cleaned_data['textRecommander'])
                return False
            return True
        else:
            print self.errors
        return False
