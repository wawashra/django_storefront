from typing import Any, List, Optional, Tuple
from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models
# Register your models here.


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    search_fields = ['title']
    @admin.display(ordering='products_count')
    def products_count(self, colletion):

        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(colletion.id)
            }))

        return format_html('<a href="{}">{}</a>', url, colletion.products_count)
        # return colletion.products_count

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        ).order_by('products_count')


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return [
            ('<10', 'Low'),
            ('>10', 'Higth')
        ]

    def queryset(self, request: Any, queryset: QuerySet) -> Optional[QuerySet]:
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)
        elif self.value() == ">10":
            return queryset.filter(inventory__gt=10)




@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']

    actions = ['clear_inventory']
    
    search_fields = ['title']
    
    fields = []

    exclude = []

    prepopulated_fields = {
        'slug' : ['title']
    }
    
    autocomplete_fields = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self, product) -> str:
        if product.inventory < 10:
            return 'Low'
        return 'Higth'

    def collection_title(self, product) -> str:
        return product.collection.title

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request: HttpRequest, querySet: QuerySet):
        updated_count = querySet.update(inventory=0)

        self.message_user(
            request,
            f'{updated_count} products were succssfuly updated',
            # messages.ERROR
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10

    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    ordering = ['first_name', 'last_name']

    def orders_count(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))

        return format_html('<a href="{}">{}</a>', url, customer.orders_count)
        # return order.orders_count

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 10
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']