# -*- coding: utf-8; -*-
from django.contrib.syndication.feeds import Feed
from portfolio.creabook.models import BookEntry
from django.utils.feedgenerator import Atom1Feed
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django.http import Http404

class RssFeed(Feed):
    def get_object(self,bits):
        domain = RequestSite(self.request).domain.split(':')[0]
        try:
            user = User.objects.get(profile__site__domain=domain)
            user.domain = domain
            return user
        except:
            raise Http404

    def title(self,obj):
        return "Projets de %s %s" % (obj.first_name.capitalize(), obj.last_name.upper())

    def description(self,obj):
        return "Derniers projets de %s %s" % (obj.first_name.capitalize(), obj.last_name.upper())


    def link(self,obj):
        return "http://%s/crealio/" % obj.domain

    def items(self,obj):
        return BookEntry.objects.filter(user=obj).order_by('-date')[:5]

    def item_link(self,obj):
        """
        Returns the URL for every item in the feed.
        """
        return "http://%s/crealio/" % (obj.user.get_profile().site.domain)


class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    subtitle = RssFeed.description
