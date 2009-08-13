# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib import auth
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.contrib.sites.models import RequestSite
from django.contrib.auth.forms import AuthenticationForm

import sha

from portfolio.settings import SECRET_KEY as salt, SITE_ID, SITE_NAME, DOMAIN_NAME, SITE_URL, ADMINS
from portfolio.commercial.forms import LoginForm
from portfolio.commercial.forms import contactForm
from portfolio.pages.models import Page
from portfolio.statistic.models import Statistics
from portfolio.decorator import commercial_site

# Connection
def login(request):
    if request.method == "POST":    
        loginform = LoginForm(request.POST)
        if loginform.login(request):            
            return HttpResponseRedirect('/administration/')
    else:
        loginform = LoginForm()
    return render_to_response('commercial/login.html', {'form': loginform, 'title': 'Connexion', 'section': 'connexion'}, context_instance=RequestContext(request))

# Inscription
@commercial_site
def inscription(request):
    page = Page.objects.get(slug="inscription",site__pk=SITE_ID)
    return render_to_response('commercial/inscription.html', 
                              {'page': page,
                               'section': 'inscription'}, 
                              context_instance=RequestContext(request))

@commercial_site
def valide(request, id, clef):
    user = get_object_or_404(User, pk=id)
    if user and not user.is_active:
        date = user.date_joined.replace(microsecond=0)
        key = sha.new((u'%s%s%s' % (salt, user, date)).encode('utf-8')).hexdigest()
        if key == clef:
            user.is_active = True
            user.save()
            
            # Création du site
            # 1. first_name.last_name.SITENAME
            # 2. first_name-last_name.SITENAME
            # 3. first_nameLast_name.SITENAME
            # 4. username.SITENAME
            # 5. usernameId.SITENAME

            # 1. first_name.last_name.SITENAME
            domain = u"%s.%s.%s" % (slugify(user.first_name), slugify(user.last_name), DOMAIN_NAME)
            print u'1. %s' % domain
            if Site.objects.filter(domain__exact=domain).count() > 0:
                # 2. first_name-last_name.SITENAME
                domain = u"%s-%s.%s" % (slugify(user.first_name), slugify(user.last_name), DOMAIN_NAME)
                print u'2. %s' % domain
                if Site.objects.filter(domain__exact=domain).count() > 0:
                    # 3. first_nameLast_name.SITENAME
                    domain = u"%s%s.%s" % (slugify(user.first_name), slugify(user.last_name), DOMAIN_NAME)
                    print u'3. %s' % domain
                    if Site.objects.filter(domain__exact=domain).count() > 0:
                        # 4. username.SITENAME
                        domain = u"%s.%s" % (slugify(user.username), DOMAIN_NAME)
                        print u'4. %s' % domain
                        if Site.objects.filter(domain__exact=domain).count() > 0:
                            # 5. usernameId.SITENAME
                            domain = u"%s%s.%s" % (slugify(user.username), str(user.id), DOMAIN_NAME)
                            print u'5. %s' % domain

            site = Site(name="%s %s - %s - %s" % (user.first_name, user.last_name, user.username, str(user.id)), domain=domain)
            site.save()

            profile = user.get_profile()
            profile.site = site
            profile.save()

            # Création des pages par défaut (Accueil, Contact)
            home_content = render_to_string('commercial/default/home_content.html', {'user': user,'site': SITE_NAME}).encode('utf-8')
            home = Page(title='Accueil', 
                        slug='accueil', 
                        onglet=1, 
                        pub_date=user.date_joined, 
                        content=home_content,
                        actif=True,
                        user=user,
                        site=site)
            home.save()

            contact_content = render_to_string('commercial/default/contact_content.html', 
                                               {'user': user,'site': SITE_NAME}).encode('utf-8')

            contact = Page(title='Contact', 
                           slug='contact', 
                           onglet=4, 
                           pub_date=user.date_joined,
                           content=contact_content,
                           actif=True,
                           user=user,
                           site=site)
            contact.save()
            
            return HttpResponseRedirect('http://%s/administration/' % (domain))

    return render_to_response('commercial/bad_request.html', {'title': 'Inscription', 'section': 'inscription'}, context_instance=RequestContext(request))

def contact(request):
    current_domain = RequestSite(request).domain.split(':')[0]
    commercial_domain = Site.objects.get(pk=SITE_ID).domain

    mails = []
    if current_domain not in [commercial_domain, u"www.%s" % commercial_domain]:
        template = 'commercial/contacts.html'
        page = get_object_or_404(Page, slug='contact', site__domain__exact=current_domain)
        mails.append(page.user.email)
    else:
        template = 'commercial/commercial_contacts.html'
        mails = [a[1] for a in ADMINS]
        page = None

    if request.method == "POST":    
        contactform = contactForm(request.POST)
        if contactform.send(mails):
            return render_to_response(template, {'title': 'Contact', 'section': 'contact', 'error': False, 'page': page, 'status': u'Mail envoyé'}, context_instance=RequestContext(request))
        else:
            return render_to_response(template, {'title': 'Contact', 'section': 'contact', 'page': page, 'error': True, 'status': u'Erreur lors de l\'envoi du mail'}, context_instance=RequestContext(request))
    else:
        contactform = contactForm()
	
	if page == None:
	    return render_to_response(template, {'title': 'Contact', 'section': 'contact', 'page': page}, context_instance=RequestContext(request))

    return render_to_response(template, 
                              {'title': 'Contact', 
                               'section': 'contact', 
                               'page': page,}, 
                              context_instance=RequestContext(request))


@commercial_site
def annuaire(request):
    last5 = Site.objects.filter(pk__gt=1).order_by('-profile__user__last_login')[:5]
    for site in last5:
        site.user = User.objects.get(profile__site=site)

    top6 = Statistics.plus_vus()
    for site in top6:
        site.user = User.objects.get(profile__site=site)

    sites = Site.objects.filter(pk__gt=1).order_by('domain')
    for site in sites:
        site.user = User.objects.get(profile__site=site)

    return render_to_response('commercial/rechercher.html', 
                              {'title': 'Rechercher', 
                               'section': 'rechercher', 
                               'last5': last5,
                               'top6': top6,
                               'sites': sites,
                               'image': 'skins/crealio/img/Admin_Photo_User.png',}, 
                              context_instance=RequestContext(request))

@commercial_site
def presentation(request):
    pages = Page.objects.filter(slug__startswith='presentation_', site__pk=SITE_ID).order_by('onglet','pk')

    return render_to_response('commercial/presentation.html', 
                              {'title': 'Présentation', 
							   'section': 'presentation', 
                               'pages': pages}, 
                              context_instance=RequestContext(request))
                              
@commercial_site
def tutoriels(request):
    pages = Page.objects.filter(slug__startswith='presentation_', site__pk=SITE_ID).order_by('onglet','pk')

    return render_to_response('commercial/tutoriels.html', 
                              {'title': 'Tutoriels', 'section': 'tutoriels', 
                               'pages': pages}, 
                              context_instance=RequestContext(request))
                                                            
@commercial_site
def rechercher(request):
    return render_to_response('commercial/recherche_google.html', 
                              {'title': 'Recherchez un Curriculum Vitæ',
                               'section': 'rechercher'}, 
                              context_instance=RequestContext(request))

@commercial_site
def connexion(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            site = Site.objects.get(profile__user__username=request.POST['username'])
            return HttpResponseRedirect('http://%s/administration/' % site) 
        else:
            error = "Compte non validé"
    else:
        error = "Compte inexistant"

    return render_to_response('commercial/login.html',
                              {'error': error},
                              context_instance=RequestContext(request))
                              
@commercial_site
def plan(request):
	
    sites = Site.objects.filter(pk__gt=1).order_by('domain')
    for site in sites:
        site.user = User.objects.get(profile__site=site)

    return render_to_response('commercial/plan.html', 
                              {'title': 'Plan du Site', 
                               'section': 'plan',
                               'sites': sites,}, 
                              context_instance=RequestContext(request))
	
@commercial_site
def partenaires(request):

    sites = Site.objects.filter(pk__gt=1).order_by('domain')
    for site in sites:
        site.user = User.objects.get(profile__site=site)

    return render_to_response('commercial/partenaires.html', 
                              {'title': 'Nos partenaires', 
                               'section': 'partenaires',
                               'sites': sites,}, 
                              context_instance=RequestContext(request))

