# -*- coding: utf-8; -*-

from portfolio.pages.forms import PageForm
from portfolio.pages.models import Page
from portfolio.settings import SITE_ID

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import RequestSite, Site
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

# Ici pas de décorator, car on peut avoir des pages dans le site commercial

# Affiche une page
def page(request, page_slug):
    domain = RequestSite(request).domain.split(':')[0]
    page = get_object_or_404(Page, slug=page_slug, site__domain__exact=domain, actif=True)

    commercial_domain = Site.objects.get(pk=SITE_ID).domain

    # Si on est sur un site avec un domaine donc portfolio
    if domain not in [commercial_domain, u"www.%s" % commercial_domain]:
        template = 'pages/aff_pages.html'
        
        return render_to_response(template, 
                              {'page': page,
                               'infos': page.user.get_profile()},
                              context_instance=RequestContext(request))

    #Sinon on est sur le site commercial, donc la page d'accueil
    else:
        return render_to_response('../templates/commercial/accueil.html', 
                                  {'page': page,
                                   'title': 'Accueil', 
                                   'section': 'accueil'}, 
                                  context_instance=RequestContext(request))

@login_required
def admin(request, page_slug):
    domain = RequestSite(request).domain.split(':')[0]
    try:
        # Modification de page
        page = Page.objects.get(slug=page_slug, site__domain__exact=domain)
        data = {'onglet': (page.onglet != 0), 'title': page.title, 'intro': page.intro, 'content': page.content, 'actif': page.actif}
    except:
        # Nouvelle page
        page = None
    site = get_object_or_404(Site, domain__exact=domain)

    # Test des droits de modification et d\'ajout
    if site != request.user.get_profile().site and not request.user.is_superuser:
        # Ce n'est pas son site et il n'est pas administrateur
        return HttpResponseRedirect('../')
        

    if request.method == 'POST':
        data = request.POST.copy()

        if 'onglet' in data:
            if page:
                data['onglet'] = page.onglet
            else:
                data['onglet'] = 1
        else:
            data['onglet'] = 0
        
        form = PageForm(data, instance=page)
        if form.is_valid(): 
            instance = form.save(commit=False)
            instance.onglet = data['onglet']
            instance.slug = page_slug
            instance.user = request.user
            instance.site = site
            instance.save()
            
            return HttpResponseRedirect('../')
    else:
        if page:
            form = PageForm(data,instance=page)
        else:
            form = PageForm(data)

    return render_to_response('pages/admin_pages.html', 
                              {'form': form,
                               'page': page,}, 
                              context_instance=RequestContext(request))
          