# -*- coding: utf-8; -*-

from portfolio.cv.models import Field, Item
from portfolio.pages.models import Page
from portfolio.cv.forms import FieldForm, ItemForm

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import RequestSite, Site
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

# Affiche le Curriculum Vitæ
def cv(request):
    domain = RequestSite(request).domain.split(':')[0]
    page = get_object_or_404(Page, slug='cv', site__domain__exact=domain, actif=True)
    fields = Field.objects.filter(user=page.user).order_by('order')
    
    for field in fields:
        field.items = Item.objects.filter(field=field.id).order_by('order')
    
    return render_to_response('cv/cv.html',
                              {'page': page,
                               'infos': page.user.get_profile(),
                               'user_cv': page.user,
                               'fields': fields,},
                               context_instance=RequestContext(request))

# Administration du Curriculum Vitæ
@login_required
def admin(request):
    # On récupère le nom de domaine et la page CV du domaine
    domain = RequestSite(request).domain.split(':')[0]
    site = get_object_or_404(Site, domain__exact=domain)
    
    current_field = None
    
    try:
        page = Page.objects.get(slug='cv', site__domain__exact=domain)
    except:
        page = Page(slug='cv',title='Curriculum Vitæ',content='<p></p>',onglet=2,actif=True,site=site,user=request.user)
        page.save()
        page = Page.objects.get(slug='cv', site__domain__exact=domain)
    
    if request.POST:
        # On a envoyé un formulaire
        if 'field' in request.POST:
            field_edit = None
            if 'field_pk' in request.POST:
                # Édition d'un field
                try:
                    field_edit = Field.objects.get(pk=request.POST['field_pk'])
                except:
                    field_edit = None
            
            field_form = FieldForm(request.POST,instance=field_edit)
            
            if field_form.is_valid():
                instance = field_form.save(commit=False)
                instance.user  = request.user
                instance.order = request.POST['order']
                instance.slug  = slugify(request.POST['title'])
                instance.save()
                field_edit = Field.objects.get(pk=instance.pk)
                return HttpResponseRedirect('/administration/cv/infos/#field_%s' % instance.pk)
        
        if 'item' in request.POST:
            item_edit = None
            if 'item_pk' in request.POST:
                # Edition d'un item
                try:
                    item_edit = Item.objects.get(pk=request.POST['item_pk'])
                except:
                    item_edit = None
            
            item_form = ItemForm(request.POST,instance=item_edit)
            
            if item_form.is_valid():
                instance = item_form.save(commit=False)
                field = Field.objects.get(pk=request.POST['field_pk'])
                instance.field = field
                instance.slug = slugify(request.POST['title'])
                instance.order = int(request.POST['order'])
                instance.save()
                return HttpResponseRedirect('/administration/cv/infos/#field_%s' % request.POST['field_pk'])
        
        if 'item_suppr' in request.POST:
            print "suppression d'item"
            try:
                item_suppr = Item.objects.get(pk=request.POST['item_pk'])
                item_suppr.delete()
            except:
                pass
        
        
        if 'field_suppr' in request.POST:
            print "suppression de field"
            try:
                field_suppr = Field.objects.get(pk=request.POST['field_pk'])
                field_suppr.delete()
            except:
                pass
        
    
    # Pour chaque Fields on cherche le formulaire et les formulaires
    # des items
    forms = []
    i = 0
    
    fields = Field.objects.filter(user=page.user).order_by('order')
    print fields
    
    for field in fields:
        # On ajoute un field
        forms.append({'cv_field': field, 'form': FieldForm(instance=field), 'items': []})
        if request.POST and 'field' in request.POST:
            if field.pk == field_form.instance.pk:
                forms[i] = {'cv_field': field, 'form': FieldForm(request.POST,instance=field_edit), 'items': []}
        
        # On récupère les items
        items = Item.objects.filter(field=field.id).order_by('order')
        j = 0
        for item in items:
            # On ajoute les items
            forms[i]['items'].append({'item': item, 'form':ItemForm(instance=item)})
            if request.POST and 'item' in request.POST:
                if item.pk == item_form.instance.pk:
                    forms[i]['items'][j]['form'] = ItemForm(request.POST,instance=item_edit)
            j += 1
        # On ajoute un formulaire vide à la fin
        forms[i]['items'].append({'item': None, 'form':ItemForm()})
        forms[i]['items'][j]['form'].order = j+1
        i += 1
    
    # On ajoute un formulaire de Field vide à la fin
    forms.append({'cv_field': None, 'form': FieldForm(), 'items': []})
    forms[i]['form'].order = i+1
    
    return render_to_response('cv/admin.html',
                              {'page': page,
                               'forms': forms},
                              context_instance=RequestContext(request))


@login_required
def organisation(request):
    domain = RequestSite(request).domain.split(':')[0]
    page = get_object_or_404(Page, slug='cv', site__domain__exact=domain, actif=True)

    if request.method == "POST":
        print request.POST
        # On récupère tous les onglets
        fields = Field.objects.filter(user=page.user).order_by('order') 
        # Pour chaque onglet
        f_num = 0
        
        for field in fields:
            f_num += 1
            if request.POST["field_%s" % str(f_num)] != f_num:
                print request.POST["field_%s" % str(f_num)]
                print f_num
                field.order = request.POST["field_%s" % str(f_num)]
                field.save()
                
            items = Item.objects.filter(field=field.id).order_by('order')
            i_num = 0
            for item in items:
                i_num += 1
                if request.POST["item_%s_%s" % (str(f_num), str(i_num))] != i_num:
                    item.order = request.POST["item_%s_%s" % (str(f_num), str(i_num))]
                    item.save()
    
    
    fields = Field.objects.filter(user=page.user).order_by('order')
    
    f_ordre = 1
    
    for field in fields:
        field.ordre = f_ordre
        field.items = Item.objects.filter(field=field.id).order_by('order')
        
        i_ordre = 1
        for item in field.items:
            item.ordre = i_ordre
            i_ordre += 1
        f_ordre += 1
        
    
    return render_to_response('cv/organisation_cv.html',
                              {'page': page,
                               'infos': page.user.get_profile(),
                               'user_cv': page.user,
                               'fields': fields,},
                               context_instance=RequestContext(request))
                               
