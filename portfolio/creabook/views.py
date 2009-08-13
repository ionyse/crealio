# -*- coding: utf-8; -*-

from portfolio.creabook.models import BookEntry
from portfolio.creabook.forms import BookEntryForm
from portfolio.decorator import user_site
from portfolio.pages.models import Page

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import RequestSite, Site
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

# Affiche le portfolio
@user_site
def book(request):
    domain = RequestSite(request).domain.split(':')[0]
    page = get_object_or_404(Page, slug='crealio', site__domain__exact=domain, actif=True)
    book_entries = BookEntry.objects.filter(user=page.user).order_by('-date')[:20]

    return render_to_response('creabook/book.html', 
                              {'page': page,
                               'infos': page.user.get_profile(),
                               'book_entries': book_entries,},
                              context_instance=RequestContext(request))

@login_required
def liste(request):
    domain = RequestSite(request).domain.split(':')[0]
    site = get_object_or_404(Site, domain__exact=domain) 
    try:
        page = Page.objects.get(slug='crealio', site__domain__exact=domain)
    except:
        page = Page(slug='crealio',title='Crealio',content='<p></p>',onglet=3,actif=True,site=site,user=request.user)
        page.save()
        page = Page.objects.get(slug='crealio', site__domain__exact=domain)

    if request.method == "POST":
        if "suppr" in request.POST:
            try:
                entry = BookEntry.objects.get(pk=request.POST['entry_pk'])
                entry.delete()
            except:
                pass

    book_entries = BookEntry.objects.filter(user=page.user).order_by('-date')

    return render_to_response('creabook/liste.html', 
                              {'page': page,
                               'infos': page.user.get_profile(),
                               'book_entries': book_entries,},
                              context_instance=RequestContext(request))

@login_required
def new(request):
    domain = RequestSite(request).domain.split(':')[0]
    site = get_object_or_404(Site, domain__exact=domain) 
    try:
        page = Page.objects.get(slug='crealio', site__domain__exact=domain)
    except:
        page = Page(slug=page_slug,title='Crealio',content='<p></p>',onglet=3,actif=True,site=site,user=request.user)
        page = Page.objects.get(slug='crealio', site__domain__exact=domain)

    
    form = None

    if request.method == "POST":
        form = BookEntryForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.slug = slugify(request.POST['title'])
            instance.site = site
            instance.save()
            return HttpResponseRedirect('../')

    if not form:
        form = BookEntryForm()

    return render_to_response('creabook/new.html', 
                              {'page': page,
                               'form': form,},
                              context_instance=RequestContext(request))

@login_required
def edit(request,id):
    domain = RequestSite(request).domain.split(':')[0]
    site = Site.objects.get(domain__exact=domain)

    entry = get_object_or_404(BookEntry, pk=int(id))
    form = None

    if request.method == "POST":
        form = BookEntryForm(request.POST, request.FILES, instance=entry)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.slug = slugify(request.POST['title'])
            instance.site = site
            instance.save()
            return HttpResponseRedirect('../')

    if not form:
        form = BookEntryForm(instance=entry)

    return render_to_response('creabook/modif.html', 
                              {'form': form,},
                              context_instance=RequestContext(request))

