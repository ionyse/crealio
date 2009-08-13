# -*- coding: utf-8 -*-
from portfolio.pages.models import Page
from portfolio.settings import SITE_ID, SITE_NAME, DOMAIN_NAME, SITE_URL, SECRET_KEY as salt

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite, Site
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from portfolio.administration.forms import AccueilContactForm, InformationForm, CvPortfolioForm, IdentiteForm, EmailForm
from portfolio.commercial.forms import contactForm
from django.http import HttpResponseRedirect

from portfolio.decorator import admin_site, user_site
import datetime
import sha


@admin_site
def profil(request):
    current_domain = RequestSite(request).domain.split(':')[0]
    # Test de la connexion + Test d'appartenance
    is_online_cv = is_online_crealio = False
    is_cv = (Page.objects.filter(slug='cv',site__domain__exact=current_domain).count() != 0)
    if is_cv:
        is_online_cv = Page.objects.get(slug='cv',site__domain__exact=current_domain).actif
    
    is_crealio = (Page.objects.filter(slug='crealio',site__domain__exact=current_domain).count() != 0)
    if is_crealio:
        is_online_crealio = Page.objects.get(slug='crealio',site__domain__exact=current_domain).actif

    status = None

    if request.method == "GET":
        if "status" in request.GET:
            status = request.GET['status']


    return render_to_response('administration/index.html', 
                              {'is_cv': is_cv, 
                               'is_crealio': is_crealio,
                               'is_online_cv': is_online_cv, 
                               'is_online_crealio': is_online_crealio,
							   'id': request.user.get_profile().identite,
                               'status': status},

                              context_instance=RequestContext(request))

@admin_site
def apparence(request):
    current_domain = RequestSite(request).domain.split(':')[0]
    # commercial_domain = SITE_URL[7:]
    commercial_domain = Site.objects.get(pk=SITE_ID).domain
    
    if request.method == "POST":
        print request.POST
        # On récupère tous les onglets
        onglets_list = Page.objects.filter(site__domain__exact=current_domain, onglet__gt=0).order_by('onglet')        
        # Pour chaque onglet
        num = 0
        for onglet in onglets_list:
            num += 1
            if request.POST[str(num)] != onglet.onglet:
                onglet.onglet = request.POST[str(num)]
                onglet.save()
                
                
    onglets = Page.objects.filter(site__domain__exact=current_domain, onglet__gt=0).order_by('onglet')
    num = 0
    for onglet in onglets:
        onglets[num].onglet = num+1
        num += 1


    return render_to_response('administration/apparence.html', {'onglets_list': onglets}, context_instance=RequestContext(request))


@admin_site
def modifAccueilContact(request,page_slug):
    domain = RequestSite(request).domain.split(':')[0]

    # Modification de page
    page = Page.objects.get(slug=page_slug, site__domain__exact=domain)
    site = get_object_or_404(Site, domain__exact=domain)    
    form = None

    if request.method == 'POST':
        form = AccueilContactForm(request.POST, instance=page)
        if form.is_valid(): 
            instance = form.save(commit=False)
            instance.onglet = page.onglet
            instance.slug   = page_slug
            instance.user   = request.user
            instance.actif  = True
            instance.site   = site
            instance.save()
            return HttpResponseRedirect('/administration/')

    if not form:
        form = AccueilContactForm(instance=page)
        

    return render_to_response('administration/pages/modifAccueil.html', 
                              {'form': form,
                               'page': page,}, 
                              context_instance=RequestContext(request))


@admin_site
def modifCvPortfolio(request,page_slug):
    domain = RequestSite(request).domain.split(':')[0]
    site = get_object_or_404(Site, domain__exact=domain) 
    # Modification de page
    try:
        page = Page.objects.get(slug=page_slug, site__domain__exact=domain)
    except:
        if page_slug == 'cv':
            page = Page(slug=page_slug,title='Curriculum Vitæ',content='<p></p>',onglet=2,actif=True,site=site,user=request.user)
        else:
            page = Page(slug=page_slug,title='Crealio',content='<p></p>',onglet=3,actif=True,site=site,user=request.user)
        page.save()
        page = Page.objects.get(slug=page_slug, site__domain__exact=domain)
    
       
    form = None

    if request.method == 'POST':
        form = CvPortfolioForm(request.POST, instance=page)
        if form.is_valid(): 
            instance = form.save(commit=False)
            instance.onglet = page.onglet
            instance.slug = page_slug
            instance.user = request.user
            instance.site = site
            instance.save()
            return HttpResponseRedirect('/administration/')

    if not form:
        form = CvPortfolioForm(instance=page)
        

    return render_to_response('administration/pages/modifAccueil.html', 
                              {'form': form,
                               'page': page,}, 
                              context_instance=RequestContext(request))

@admin_site
def onOffPage(request, page_slug):
    domain = RequestSite(request).domain.split(':')[0]
    site = get_object_or_404(Site, domain__exact=domain) 
    # Modification de page
    page = get_object_or_404(Page, slug=page_slug, site=site)

    page.actif = not page.actif
    page.save()

    return HttpResponseRedirect('/administration/')
    

@admin_site                           
def modifInformation(request):
    form = None

    if request.method == 'POST':
        form = InformationForm(request.POST, instance=request.user.get_profile())
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/administration/')

    if not form:
        form = InformationForm(instance=request.user.get_profile())
        

    return render_to_response('administration/pages/modifInformations.html', 
                              {'form': form,}, 
                              context_instance=RequestContext(request))
                        

@admin_site
def changePassword(request):
    form = None
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            logout(request)
            return HttpResponseRedirect('/administration/')

    if not form:
        form = PasswordChangeForm(request.user)

    return render_to_response('administration/change_password.html', 
                              {'form': form},
                              context_instance=RequestContext(request))

@admin_site
def changeMail(request):
    domain = RequestSite(request).domain
    form = None
    if request.method == "POST":
        form = EmailForm(request.user, domain, request.POST)

        if form.is_valid():
            form.save()
            logout(request)
            return HttpResponseRedirect('/administration/')
    if not form:
        form = EmailForm(request.user, domain)

    return render_to_response('administration/change_email.html', 
                              {'form': form},
                              context_instance=RequestContext(request))
@user_site
def valide(request, id, clef):
    user = get_object_or_404(User, pk=id)
    if user and not user.is_active:
        date = user.date_joined.replace(microsecond=0)
        key = sha.new((u'%s%s%s' % (salt, date, user)).encode('utf-8')).hexdigest()
        if key == clef:
            user.is_active = True
            user.save()
            return HttpResponseRedirect('/administration/')
    return render_to_response('commercial/bad_request.html', {'title': 'Modification de mail'}, context_instance=RequestContext(request))
        
@admin_site
def changeIdentite(request):
    form = None
    if request.method == "POST":
        form = IdentiteForm(request.POST, request.FILES, instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            return render_to_response("administration/change_identite.html",
                                      {'identite': request.user.get_profile().identite}, 
                                      context_instance=RequestContext(request))

    if not form:
        form = IdentiteForm(instance=request.user.get_profile())

    return render_to_response('administration/change_identite.html', 
                              {'form': form,
                              'identite' : request.user.get_profile().identite},
                              context_instance=RequestContext(request))

@admin_site
def supprIdentite(request):
    profil = request.user.get_profile()
    profil.identite.delete()
    profil.save()
    return HttpResponseRedirect('/administration/')

@admin_site
def suggestion(request):
    status = None
    if request.method == "POST":
        data = request.POST.copy()
        data['pseudo'] = unicode(request.user)
        data['mail'] = unicode(request.user.email)
        data['objet'] = "Suggestion"
        contactform = contactForm(data)

        if contactform.send():
            status = True
        else:
            status = False
        
    return HttpResponseRedirect('/administration/?status=%s#suggestion' % status)

@admin_site
def delete(request):
    if request.method == "POST":
        if "oui" in request.POST:
            domain = RequestSite(request).domain.split(':')[0]
            site = get_object_or_404(Site, domain__exact=domain) 
            user = get_object_or_404(User, profile__site__domain__exact=domain)

            site.delete()
            user.delete()
            # Suppression effective
            return HttpResponseRedirect('%s' % (SITE_URL))
        else:
            # Pas de suppression
            return HttpResponseRedirect('/administration/')
    else:
        # Formulaire de confirmation de suppression
        return render_to_response('administration/delete_account.html', 
                                  context_instance=RequestContext(request))
