from functools import wraps

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.urls import reverse


def is_main_domain(request):
    current_domain = get_current_site(request).domain
    main_domain = Site.objects.get(pk=settings.SITE_ID).domain
    main_domains = [main_domain, u"www.%s" % main_domain]

    return current_domain in main_domains


def user_site(func):
    @wraps(func)
    def decorator(request, *args, **kwargs):
        if not is_main_domain(request):
            return func(request, *args, **kwargs)
        else:
            raise Http404
    return decorator


def main_site(func):
    @wraps(func)
    def decorator(request, *args, **kwargs):
        if is_main_domain(request):
            return func(request, *args, **kwargs)
        else:
            raise Http404
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
                return HttpResponseRedirect('{}{}'.format(settings.SITE_URL,
                                                          reverse('login')))
