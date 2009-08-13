# -*- coding: utf-8 -*- 
from django.contrib import admin
from portfolio.statistic.models import Statistics, UserAgent, OS, Browser

class StatisticsAdmin(admin.ModelAdmin):
    ordering = ['date']
    pass

class UserAgentAdmin(admin.ModelAdmin):
    pass

class OSAdmin(admin.ModelAdmin):
    ordering = ['name', 'version']
    pass

class BrowserAdmin(admin.ModelAdmin):
    ordering = ['name', 'version']
    pass

admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(UserAgent, UserAgentAdmin)
admin.site.register(OS, OSAdmin)
admin.site.register(Browser, BrowserAdmin)
