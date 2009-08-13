# -*- coding: utf-8 -*-

from portfolio.settings import SITE_ID, SITE_NAME, DOMAIN_NAME, SITE_URL, ADMIN_MEDIA_PREFIX
from portfolio.pages.models import Page
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


def site(request):
	
    cond = conf = None
    try:
        cond = Page.objects.get(slug='conditions', site__pk=SITE_ID, actif=True)
        conf = Page.objects.get(slug='confidentialite', site__pk=SITE_ID, actif=True)
    except ObjectDoesNotExist:
        pass

    return {'SITE_NAME':  SITE_NAME,
            'DOMAIN_NAME': RequestSite(request).domain,
            'COMMERCIAL_URL': SITE_URL,
            'ADMIN_MEDIA': ADMIN_MEDIA_PREFIX,
            'path_url': request.path_info.split('/')[1],
			'cond': cond,
			'conf': conf,}

def menu(request):
    current_domain = RequestSite(request).domain.split(':')[0]
    # commercial_domain = SITE_URL[7:]
    commercial_domain = Site.objects.get(pk=SITE_ID).domain
    
    # Sinon, ça veut dire que c'est le site commercial
    if current_domain not in [commercial_domain, u"www.%s" % commercial_domain]:
        onglets = Page.objects.filter(site__domain__exact=current_domain, onglet__gt=0, actif=True).order_by('onglet')
        
        if onglets:
            return {'onglets': onglets,
                    'commercial_site': False,
                    'portfolio_name': u'%s %s' % (onglets[0].user.first_name,
                                                  onglets[0].user.last_name),
                    'user_infos': onglets[0].user,
                    'infos': onglets[0].user.get_profile()}
        else:
            return {}
    else:
        return {'commercial_site': True}
