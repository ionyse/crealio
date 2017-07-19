from smtplib import SMTPException

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.urls import reverse

from formtools.wizard.views import SessionWizardView

from .decorators import main_site
from .forms import Step1, Step2
from .models import User


@main_site
def index(request):
    return render(request, 'users/home.html', {'section': 'presentation'})


@main_site
def sign_in(request):
    return render(request, 'users/sign-in.html')


class InscriptionWizard(SessionWizardView):
    form_list = [Step1, Step2]
    template_name = 'users/step.html'

    def done(self, form_list, **kwargs):
        fields = [form.cleaned_data for form in form_list]

        site = Site.objects.get(pk=settings.SITE_ID)

        # Creation de l'utilisateur
        user = User.objects.create_user(
            fields[0]['username'],
            fields[0]['email'],
            fields[0]['password'])
        user.is_active = False
        user.first_name = fields[1]['first_name']
        user.last_name = fields[1]['last_name']
        user.site = site
        user.city = fields[1]['city']
        user.country = fields[1]['country']
        user.job = fields[1]['job']
        user.save()

        site = Site.objects.get(pk=settings.SITE_ID)

        # Envoi du mail de confirmation
        key = user.generate_key()

        subject = '[{}] : Inscription'.format(settings.SITE_NAME)
        url = '{}{}'.format(settings.SITE_URL,
                            reverse('sign-in-validation', kwargs={"id": user.id,
                                                                  "key": key}))

        mail = render_to_string(
            'users/sign-in-confirmation.html',
            {'title': subject,
             'username': user.username,
             'first_name': user.first_name,
             'site': settings.SITE_NAME,
             'url': url})

        msg = EmailMessage(subject, mail,
                           '{} <no-reply@{}>'.format(settings.SITE_NAME, settings.DOMAIN_NAME),
                           [user.email])
        msg.content_subtype = "html"  # Main content is now text/html
        try:
            msg.send()
        except (ConnectionRefusedError, SMTPException):
            # Si pas internet, on envoi pas le mail mais on écrit l'url dans le terminal
            print(url)

        return render(self.request, "users/checkmail.html",
                      {'section': 'inscription'},)


@main_site
def sign_in_validation(request, id, key):
    user = get_object_or_404(User, pk=id)
    if user and not user.is_active:
        user_key = user.generate_key()
        if user_key == key:
            user.is_active = True

            # Création du site
            # 1. first_name.last_name.SITENAME
            # 2. first_name-last_name.SITENAME
            # 3. first_nameLast_name.SITENAME
            # 4. username.SITENAME
            # 5. usernameId.SITENAME

            first_name_slug = slugify(user.first_name)
            last_name_slug = slugify(user.last_name)
            username_slug = slugify(user.username)

            # 1. firstName.lastName.SITENAME
            domain = "{}.{}.{}".format(first_name_slug,
                                       last_name_slug,
                                       settings.DOMAIN_NAME)
            if Site.objects.filter(domain__exact=domain).count() > 0:
                # 2. firstName-lastName.SITENAME
                domain = "{}-{}.{}".format(first_name_slug,
                                           last_name_slug,
                                           settings.DOMAIN_NAME)
                if Site.objects.filter(domain__exact=domain).count() > 0:
                    # 3. firstName_lastName.SITENAME
                    domain = "{}_{}.{}".format(first_name_slug,
                                               last_name_slug,
                                               settings.DOMAIN_NAME)
                    if Site.objects.filter(domain__exact=domain).count() > 0:
                        # 4. username.SITENAME
                        domain = "{}_{}.{}".format(username_slug,
                                                   settings.DOMAIN_NAME)

            site_name = "{} {} - {}".format(user.first_name, user.last_name, user.username)
            site = Site(name=site_name, domain=domain)
            site.save()

            user.site = site
            user.save()

            # Création des pages par défaut (Accueil, Contact)
            return HttpResponseRedirect('http://%s/administration/' % (domain))

    return render('users/bad_request.html', {'section': 'inscription'})
