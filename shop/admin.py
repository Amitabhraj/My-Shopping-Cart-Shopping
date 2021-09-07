from django.contrib import admin
from .models import *

admin.site.register(Order)
admin.site.register(Contact)
@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    class Media:
        js= ('My-Awesome-Cart-Website/static/tiny.js',)
