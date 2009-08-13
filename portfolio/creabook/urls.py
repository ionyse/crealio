# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from portfolio.creabook.feeds import RssFeed, AtomFeed

feeds = {
    'rss': RssFeed,
    'atom': AtomFeed,
}

urlpatterns = patterns('',
    (r'^$', 'portfolio.creabook.views.book'),  # Affichage du book
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),
)
