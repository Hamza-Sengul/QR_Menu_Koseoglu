# admin.py
from django.contrib import admin
from .models import Product, Logo, Feedback, category, ProductClick

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image', 'detail')

admin.site.register(Logo)
admin.site.register(Feedback)
admin.site.register(category)
admin.site.register(ProductClick)