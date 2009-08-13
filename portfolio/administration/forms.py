# -*- coding: utf-8 -*-

from portfolio.pages.models import Page
from portfolio.commercial.models import Profile, Pays
from django.utils.translation import ugettext_lazy as _

from portfolio.settings import SITE_NAME, DOMAIN_NAME, SITE_URL, SECRET_KEY as salt

from datetime import date
import sha
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django import forms

class AccueilContactForm(forms.ModelForm):
    class Meta:
        model   = Page
        fields  = ('title', 'content')

class CvPortfolioForm(forms.ModelForm):
    class Meta:
        model   = Page
        fields  = ('title', 'intro', 'content')
             
class InformationForm(forms.ModelForm):
    dob = forms.DateField(label="Date de naissance (10/09/1962)", input_formats=['%d/%m/%Y','%d-%m-%Y','%Y-%m-%d'], widget=forms.TextInput(attrs={'class':'vDateField'}))
    country    = forms.ModelChoiceField(label="Pays", queryset=Pays.objects.all().order_by('name'))
    cob = forms.ModelChoiceField(label="Pays de naissance", queryset=Pays.objects.all().order_by('name'))

    class Meta:
        model   = Profile
        fields  = ('address1', 'address2', 'zipcode', 'city', 'country', 'metier',
        'dob', 'pob', 'cob', 'nationality', 'd_licence', 'phone', 'mobile', 'status')

class IdentiteForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('identite')

class EmailForm(forms.Form):
    """
    A form that lets a user change his/her email by entering
    their old password.
    """
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    new_email  = forms.EmailField(label="Nouvelle adresse Email")
    new_email2 = forms.EmailField(label="Confirmation de la nouvelle adresse")

    def __init__(self, user, domain, *args, **kwargs):
        self.user = user
        self.domain = domain
        super(EmailForm, self).__init__(*args, **kwargs)

    def clean_new_email2(self):
        email1 = self.cleaned_data.get('new_email')
        email2 = self.cleaned_data.get('new_email2')
        if email1 and email2:
            if email1 != email2:
                raise forms.ValidationError("Vous n'avez pas entrez deux fois la même adresse")
        return email2

    def clean_password(self):
        """
        Validates that the password field is correct.
        """
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError(_("Your old password was entered incorrectly. Please enter it again."))
        return password

    def save(self):
        date = self.user.date_joined.replace(microsecond=0)
        key = sha.new((u'%s%s%s' % (salt, date, self.user)).encode('utf-8')).hexdigest()

        subject = u'[%s] : Changement d\'adresse email' % SITE_NAME
        url = u'http://%(url)s/%(id)d/%(key)s/' % {'url': self.domain+'/administration/email/valide',
                                            'id': self.user.id,
                                            'key': key}

        mail = render_to_string('administration/mail_change_email.html', { 'titre': subject,
                                                                       'pseudo': self.user.username,
                                                                       'first_name': self.user.first_name,
                                                                       'site': SITE_NAME,
                                                                       'url': url})

        msg = EmailMessage(subject, mail, '%(site)s <no-reply@%(domain)s>' % {'site': SITE_NAME, 'domain': DOMAIN_NAME}, [self.cleaned_data.get('new_email')])
        msg.content_subtype = "html"  # Main content is now text/html
        try:
            msg.send()
        except:
            # Si pas internet, on envoi pas le mail mais on écrit l'url dans le terminal
            print url

        self.user.email = self.cleaned_data.get('new_email')
        self.user.is_active = False
        self.user.save()

EmailForm.base_fields.keyOrder = ['password', 'new_email', 'new_email2']
