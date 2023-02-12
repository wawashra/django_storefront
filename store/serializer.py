from rest_framework import serializers
from .models import Product, Collection, Review
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title', 'products_count')
        
    # if we need overwite somethng ?    
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    
    products_count = serializers.IntegerField(read_only=True)



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'inventory', 'description', 'unit_price', 'price_with_tax', 'collection')
        
    # No need
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, source='unit_price'
    # )
    # price_with_tax = serializers.SerializerMethodField(
    #     method_name='calculate_tax'
    # )
    # collection_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )
    # collection_name = serializers.StringRelatedField(
    #     source='collection'
    # )
    # collection = CollectionSerializer()
    # collection_htys = serializers.HyperlinkedRelatedField(
    #     source='collection',
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax'
    )

    def calculate_tax(self, product: Product) -> Decimal:
        return product.unit_price * Decimal(1.1)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)