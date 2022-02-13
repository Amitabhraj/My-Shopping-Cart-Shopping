from django.contrib import admin
from .models import *

admin.site.register(Order)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(Category)
@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinymce.js',)
