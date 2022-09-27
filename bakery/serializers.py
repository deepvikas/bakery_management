from rest_framework import serializers

from . models import Discount, Product, Order

class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = ['id', 'discount_rule', 'discount_value', 'message', 'is_enable']

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'cost_price', 'selling_price', 'description', 'barcode', 'quantity', 'discount_id']


    def update(self,  instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'quantity', 'user_id', 'order_date', 'amount']

