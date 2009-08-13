from django.contrib import admin
from portfolio.creabook.models import BookEntry

class BookEntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    
    list_display = ('title','user','date')
    list_filter = ['title','user','date']
    search_fields = ['title','user']
    
    class Media:
        js = (
                "medias/jscripts/tiny_mce/tiny_mce.js",
                "medias/jscripts/tiny_conf.js",
             )

admin.site.register(BookEntry, BookEntryAdmin)
