from django.db.models import Q, F
from django.db.models.aggregates import Count, Sum, Min, Max, Avg
from django.db.models.expressions import ExpressionWrapper, Func, Value
from django.db.models.fields import DecimalField
from django.db.models.functions import Concat
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Cart, CartItem, Order, OrderItem, Product, Customer, Collection
from tags.models import Tag, TaggedItem


def say_hello(request):
    # q_set = Product.objects.select_related('collection').all()
    # q_set = Product.objects.prefetch_related('promotions').all()
    # q_set = Product.objects.prefetch_related('promotions').select_related('collection').all()
    # 'products': list(q_set)
    '''Get the last 5 order with their customer and item -include product'''
    # q_set = Order.objects.select_related('customer').prefetch_related(
    #     'orderitem_set__product').order_by('-placed_at')[:5]
    q_set = Product.objects.annotate(
        total_sales=Sum(F('orderitem__unit_price')*F('orderitem__quantity'))
    ).order_by('-total_sales')[:5]
    print(TaggedItem.objects.get_tags_for(Product, 1))
    return render(request, 'hello.html')


# Customers with .com accounts
def get_customers_with_dot_com():
    query_set = Customer.objects.filter(email__icontains='.com')
    return query_set

# Collections that don’t have a featured product


def get_collections_dont_has_fp():
    return Collection.objects.filter(featured_product_id__isnull=True)


# Products with low inventory (less than 10)
def get_low_inventory_products(min_inventory):
    return Product.objects.filter(inventory__lt=min_inventory)


# Orders placed by customer with id = ?
def get_customer_orders_by_id(id):
    return Order.objects.filter(customer_id=id)

# Order items for products in collection id = ?


def get_orders_in_collection(id):
    return OrderItem.objects.filter(product__collection__id=id)


''' Products that have been ordered and sorted by the title'''


def get_ordered_product():
    # get all ordered product ids from order_item and remove duplicate ids
    ordered_products = OrderItem.objects.values('product_id').distinct()
    # return ordered product
    return Product.objects.filter(id__in=ordered_products).order_by('title')


'''Aggregating Objects'''


def get_agg():
    res = {}
    # How many orders do we have?
    res['order_count'] = Order.objects.aggregate(count=Count('id'))
    # How many units of product 1 have we sold?
    res['units_of_product_one'] = OrderItem.objects.filter(
        product__id=1).aggregate(unit_solid=Sum('quantity'))
    # How many orders has customer 1 placed?
    res['cus_one_order'] = Order.objects.filter(
        customer__id=1).aggregate(count=Count('id'))
    # What is the min, max and average price of the products in collection 3?
    res['prod_on_coll_one'] = Product.objects.filter(collection__id=3).aggregate(
        min_p=Min('unit_price'), max_p=Max('unit_price'), avg_p=Avg('unit_price'))
    return res


def call_db_func():
    q_set = Customer.objects.annotate(
        full_name=Func(F('first_name'), Value(
            ' '), F('las_name'), function='CONCAT')
    )

    # or
    q_set = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' ', 'last_name'))
    )


def get_customers_and_count_number_of_orders():
    Customer.objects.annotate(
        orders_count=Count('order')  # but why not order_set ?
    )


'''Working with Expression Wrappers'''


def working_with_expression_wrappers():
    discounted_price_exp = ExpressionWrapper(
        F('unit_price') * 0.8, output_field=DecimalField()
    )
    q_set = Product.objects.annotate(
        discounted_price=discounted_price_exp
    )
    # Customers with their last order ID
    q_set = Customer.objects.annotate(
        last_order_id=Max('order__id')
    )
    # Collections and count of their products
    q_set = Collection.objects.annotate(
        product_count=Count('product')
    )
    # Customers with more than 5 orders
    Customer.objects.annotate(
        order_count=Count('order')
    ).filter(order_count__gt=5)
    # Customers and the total amount they’ve spent
    q_set = Customer.objects.annotate(
        total_spent=Sum(F('order__orderitem__unit_price')
                        * F('order__orderitem__quantity'))
    )
    # Top 5 best-selling products and their total sales
    Product.objects.annotate(
        total_sales=Sum(F('orderitem__unit_price')*F('orderitem__quantity'))
    ).order_by('-total_sales')[:5]


'''Querying Generic Relationships'''


def q_g_r():
    content_type = ContentType.objects.get_for_model(Product)
    return TaggedItem.objects \
        .select_related('tag') \
        .filter(
            content_type=content_type,
            object_id=1  # product_id
        )

# create order and item with in Transactions method 1


@transaction.atomic
def c_o_i_w_transactions_one():
    order = Order()
    order.customer_id = 1
    order.save()

    item = CartItem()
    item.order = order
    item.product_id = 1
    item.quantity = 1
    item.unit_price = 10
    item = item.save()

# create order and item with in Transactions method 2


def c_o_i_w_transactions_two():
    # ...
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = CartItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item = item.save()


# Create a shopping cart with an item


def c_s_c_w_item():
    cart = Cart()
    cart.save()

    item1 = CartItem()
    item1.cart = cart
    item1.product_id = 1
    item1.quantity = 1
    item1 = item1.save()
# Update the quantity of an item in a shopping cart


def u_item():
    item = CartItem.objects.filter(pk=1)
    item.quantity = 2
    item.save()
# Remove a shopping cart with its items


def d_cart():
    cart = Cart(pk=1)
    cart.delete()
