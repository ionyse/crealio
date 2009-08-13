# -*- coding: utf-8 -*-

from django import forms
from django.contrib.formtools.wizard import FormWizard

from portfolio.commercial.models import Profile, Pays
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from portfolio.settings import SITE_ID, SITE_NAME, DOMAIN_NAME, SITE_URL, SECRET_KEY as salt, ADMINS

from datetime import date
import sha
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

from django.utils.translation import ugettext_lazy as _, ugettext
from django.template import RequestContext

class Step1(forms.Form):
    username        = forms.CharField(label='Identifiant')
    password        = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    conf_password   = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)
    email           = forms.EmailField(label='Email')
    conf_email      = forms.EmailField(label='Confirmer l\'email')
    cgu             = forms.BooleanField(label='J\'accepte les conditions générales d\'utilisations',)
    
    def clean_username(self):
        user = User.objects.filter(username=self.cleaned_data['username'])
        if user:
            raise forms.ValidationError("Cet identifiant est déjà  utilisé par un utilisateur")
        else:
            return self.cleaned_data['username']
    
    def clean_conf_password(self):
        if self.cleaned_data['password'] == self.cleaned_data['conf_password']:
           return self.cleaned_data['password']
        raise forms.ValidationError("Vous n\'avez pas entré deux fois le même mot de passe")
         
    def clean_conf_email(self):
        if self.cleaned_data['email'].lower() == self.cleaned_data['conf_email'].lower():
            return self.cleaned_data['email'].lower()
        raise forms.ValidationError("Vous n\'avez pas entré deux fois la même adresse email")
    
class Step2(forms.ModelForm):
    first_name = forms.CharField(label='Prénom')
    last_name  = forms.CharField(label='Nom')
    country    = forms.ModelChoiceField(label="Pays", queryset=Pays.objects.all().order_by('name'))

    class Meta:
        model   = Profile
        fields  = ('first_name', 'last_name', 'city', 'country', 'metier')

Step2.base_fields.keyOrder = ['first_name', 'last_name', 'city', 'country', 'metier']

class InscriptionWizard(FormWizard):
    def done(self, request, form_list):
        champs = [form.cleaned_data for form in form_list]
        # Creation de l'utilisateur
        user = User.objects.create_user(champs[0]['username'], champs[0]['email'], champs[0]['password'])
        user.is_active = False
        user.first_name = champs[1]['first_name']
        user.last_name = champs[1]['last_name']
        user.save()

        site = Site.objects.get(pk=SITE_ID)

        # Creation du profile
        p = Profile( user       = user, 
                     site       = site,
                     city       = champs[1]['city'],
                     country    = champs[1]['country'],
                     metier     = champs[1]['metier'],
                  )
        p.save()

        # Envoi du mail de confirmation
        date = user.date_joined.replace(microsecond=0)
        key = sha.new((u'%s%s%s' % (salt, user, date)).encode('utf-8')).hexdigest()

        subject = u'[%s] : Inscription' % SITE_NAME
        url = u'%(url)s/%(id)d/%(key)s/' % {'url': SITE_URL+'/inscription/valide',
                                            'id': user.id,
                                            'key': key}

        mail = render_to_string('commercial/mail_conf_inscription.html', { 'titre': subject,
                                                                           'pseudo': user.username,
                                                                           'first_name': user.first_name,
                                                                           'site': SITE_NAME,
                                                                           'url': url})

        msg = EmailMessage(subject, mail, '%(site)s <no-reply@%(domain)s>' % {'site': SITE_NAME, 'domain': DOMAIN_NAME}, [user.email])
        msg.content_subtype = "html"  # Main content is now text/html
        try:
            msg.send()
        except:
            # Si pas internet, on envoi pas le mail mais on écrit l'url dans le terminal
            print url

        return render_to_response("commercial/checkmail.html", {'title': 'Inscription', 'section': 'inscription'}, context_instance=RequestContext(request))

    def get_template(self, step):
        return ['commercial/step%s.html' % step, 'commercial/step.html']

class LoginForm(forms.Form):
        username = forms.CharField(label=_('Username'))
        password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)        
        user = None   # allow access to user object
        def clean(self):
            # only do further checks if the rest was valid
            if self._errors: return
            
            from django.contrib.auth import login, authenticate
            user = authenticate(username=self.data['username'],
                                password=self.data['password'])
            if user is not None:
                if user.is_active:
                    self.user = user                    
                else:
                    raise forms.ValidationError(ugettext(
                        'This account is currently inactive. Please contact '
                        'the administrator if you believe this to be in error.'))
            else:
                raise forms.ValidationError(ugettext(
                    'The username and password you specified are not valid.'))

        def login(self, request):
            from django.contrib.auth import login
            if self.is_valid():
                login(request, self.user)
                return True
            return False

class contactForm(forms.Form):
    pseudo = forms.CharField(label='Nom', required=False)
    mail = forms.EmailField(label='Email')
    objet  = forms.CharField(label='Objet', required=False)
    message = forms.CharField(label='Message',widget=forms.Textarea)

    def send(self, mails=[]):
        if self.is_valid():
            if not mails:
                mails = [a[1] for a in ADMINS]
            # Codage de l'envoi
            subject = u'[%s] : %s' % (SITE_NAME,
                                      self.cleaned_data['objet'])
            msg = EmailMessage(subject, self.cleaned_data['message'], self.cleaned_data['mail'], mails)
            try:
                msg.send()
            except:
                print "Nom : %s\nEmail : %s\nObjet : %s\nMessage : %s\n" % (self.cleaned_data['pseudo'], self.cleaned_data['mail'],self.cleaned_data['objet'],self.cleaned_data['message'])
                return False
            return True
        else:
            print self.errors
        return False
