# -*- coding: utf-8 -*-
from django.contrib.sites.models import RequestSite, Site
from django.http import HttpResponseRedirect, Http404, HttpResponse
from portfolio.settings import SITE_ID, SITE_URL

try:
    from functools import update_wrapper
except ImportError:
    from django.utils.functional import update_wrapper  # Python 2.3, 2.4 fallback.


def test_site(test_func):
    """
    Decorator for views that checks the test_func condition (in or not in)
    """
    def decorate(view_func):
        return _CheckSite(view_func, test_func)
    return decorate

def user_site(function=None):
    """
    Est-ce que ce n'est pas le site commercial
    """
    actual_decorator = test_site(lambda u,y: u not in y)
    if function:
        return actual_decorator(function)
    return actual_decorator

def commercial_site(function=None):
    """
    Est-ce le site commercial ?
    """
    actual_decorator = test_site(lambda u,y: u in y)
    if function:
        return actual_decorator(function)
    return actual_decorator

class _CheckSite(object):
    """
    On compare le nom de domaine du site à celui du site commercial
    """
    def __init__(self, view_func, test_func):
        self.view_func = view_func
        self.test_func = test_func
        update_wrapper(self, view_func)
        
    def __get__(self, obj, cls=None):
        view_func = self.view_func.__get__(obj, cls)
        return _CheckSite(view_func, self.test_func)
    
    def __call__(self, request, *args, **kwargs):
        commercial_domain = Site.objects.get(pk=SITE_ID).domain
        current_domain = RequestSite(request).domain.split(':')[0]
        commercial_ndds = [commercial_domain, u"www.%s" % commercial_domain]

        if self.test_func(current_domain, commercial_ndds):
            return self.view_func(request, *args, **kwargs)
        raise Http404


##### Admin_site decorator #####

def admin_site(view_func=None):
    """
    Decorator for views that checks that the user is admin of the
    website, displaying an error message if necessary.
    """
    def failure_func(request, *args, **kwargs):
        # On le redirige vers sa page d'administration
        try:
            domain = request.user.get_profile().site.domain
            return HttpResponseRedirect('http://%s/administration/' % domain)
        except:
            return HttpResponseRedirect('/connexion/')
    
    actual_decorator = user_passes_test(lambda u: u.admin_site, failure_func)
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def user_passes_test(test_func, failure_func):
    """
    Decorator for views that checks that the user is logged in,
    displaying the login form if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorate(view_func):
        return _CheckUserPassesTest(view_func, test_func, failure_func)
    return decorate

class _CheckUserPassesTest(object):
    """
    Decorator for views that checks that the user passes a test. If the 
    test is passed, the view function is invoked. The test should be a 
    callable that takes the user object and returns True if the user 
    passes. If the test fails, it returns a failure function defined in 
    the decorator.
    """
    def __init__(self, view_func, test_func, failure_func):
        self.view_func = view_func
        self.test_func = test_func
        self.failure_func = failure_func
        update_wrapper(self, view_func)
        
    def __get__(self, obj, cls=None):
        view_func = self.view_func.__get__(obj, cls)
        return _CheckUserPassesTest(view_func, self.test_func, self.failure_func)
    
    def __call__(self, request, *args, **kwargs):
        if self.test_func(request.user):
            return self.view_func(request, *args, **kwargs)
        return self.failure_func(request, *args, **kwargs)


