from django.contrib import admin
from portfolio.pages.models import Page

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    
    list_display = ('title','site','pub_date','onglet')
    list_filter = ['site']
    ordering = ['site', 'onglet']

    search_fields = ['title']
    
    class Media:
        js = (
                "medias/jscripts/tiny_mce/tiny_mce.js",
                "medias/jscripts/tiny_conf.js",
             )

admin.site.register(Page, PageAdmin)
