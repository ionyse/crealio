# -*- coding: utf-8; -*-

from portfolio.statistic.models import Statistics

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import RequestSite, Site
from django.db import connection
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def pages(request):
    """
    On récupère la liste des pages dans l'ordre décroissant de visualisation.
    """
    domain = RequestSite(request).domain.split(':')[0]
    site = Site.objects.get(domain__exact=domain)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT query, COUNT(*) as count
        FROM statistic_statistics
        WHERE site_id = %s
        GROUP BY query
        ORDER BY count DESC
        """, [str(site.pk)])
    stats = cursor.fetchall()

    print stats

    return render_to_response('statistic/pages.html', 
                              {'stats': stats,}, 
                              context_instance=RequestContext(request))
