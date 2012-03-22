# -*- coding: utf-8 -*-
from django.contrib.auth import logout
from django.contrib.sites.models import RequestSite, Site
from django.core.mail import send_mail

from portfolio.statistic.models import Statistics, UserAgent
from portfolio.settings import ADMINS, SITE_ID

class UserRightMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'user'), "The portfolio UserRightMiddleware requires the AuthenticationMiddleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware' before it."
        current_domain = RequestSite(request).domain.split(':')[0]
        request.user.admin_site = None     

        try:
            if request.user.is_superuser or request.user.get_profile().site.domain == current_domain:
                # Si ce n'est pas son domaine ou qu'il n'est pas admin,
                # il ne peut pas se connecter
                request.user.admin_site = True
            else:
                request.user.admin_site = False
        except AttributeError:
            pass
        return None

class StatisticsMiddleware(object):
    # A chaque requête on enregistre les informations statistiques
    def process_request(self, request):

        user_ip         = request.environ.get('REMOTE_ADDR', '')
        user_agent      = request.environ.get('HTTP_USER_AGENT', '')
        user_url        = request.path_info
        user_id	        = '0'

        # On exclus certains ensembles d'URL de manière à optimiser
        # les statistiques
        EXCLUDES = ('administration', 'admin', 'medias', '', 'icons', 'robots.txt', 'jsi18n', 'accounts', 'favicon.ico', 'media')
        if user_url.split('/')[1] in EXCLUDES:
            return None

        try:
            agent = UserAgent.objects.get(agent__exact=user_agent)
        except:
            agent = UserAgent(agent=user_agent)
            agent.save()
            agent = UserAgent.objects.get(agent__exact=user_agent)

        current_domain  = RequestSite(request).domain.split(':')[0]

        try:
            site = Site.objects.get(domain__exact=current_domain)
        except:
            return None

        if site:
            # Si c'est un site inexistant c'est pas la peine de générer une erreur
            stat = Statistics(ip = user_ip,
                              user_agent = agent,
                              query = user_url,
                              site = site,)
            stat.save()
        else:
            print current_domain

        return None
