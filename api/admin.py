from django.contrib import admin

from .models import Product, Purchase, Sell


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "slug"]


admin.site.register(Product, ProductAdmin)

admin.site.register(Purchase)
admin.site.register(Sell)
