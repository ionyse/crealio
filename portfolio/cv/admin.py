from django.contrib import admin
from portfolio.cv.models import Field, Item

class FieldAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['order']

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['field', 'order']

    class Media:
        js = (
                "jscripts/tiny_mce/tiny_mce.js",
                "jscripts/tiny_conf.js",
             )

admin.site.register(Field, FieldAdmin)
admin.site.register(Item, ItemAdmin)
