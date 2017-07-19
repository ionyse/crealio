from functools import wraps

from django.contrib.sites.models import RequestSite, Site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.settings import SITE_ID, SITE_URL
from django.urls import reverse


def is_commercial_domain(request):
    current_domain = RequestSite(request).domain.split(':')[0]
    commercial_domain = Site.objects.get(pk=SITE_ID).domain
    commercial_domains = [commercial_domain, u"www.%s" % commercial_domain]

    return current_domain in commercial_domains


def user_site(func):
    @wraps(func)
    def decorator(request, *args, **kwargs):
        if not is_commercial_domain(request):
            return func(request, *args, **kwargs)
        else:
            raise Http404
    return decorator


def commercial_site(func):
    @wraps(func)
    def decorator(request, *args, **kwargs):
        return is_commercial_domain(request)
    return decorator


def admin_site(func):
    @wraps(func)
    def decorator(request, *args, **kwargs):
        if request.user.is_admin():
            return func(request, *args, **kwargs)
        else:
            try:
                user_domain = request.user.site.domain
                return HttpResponseRedirect('https://{}{}'.format(user_domain,
                                                                  reverse('administration')))
            except ObjectDoesNotExist:
                return HttpResponseRedirect('{}{}'.format(SITE_URL, reverse('login')))
