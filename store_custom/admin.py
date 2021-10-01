from store.models import Product
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem
# Register your models here.

class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']

admin.site.unregister(Product)
@admin.register(Product)
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]