from rest_framework import serializers
from .models import Cart, CartItem , Transaction , OrderStatus




class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        # show  name and quantity and price for each item in cart
        extra_kwargs = {
            'items': {
                'read_only': True,
                'required': False,
                'allow_null': True,
                'allow_empty': True,
                'many': True,
                'lookup_field': 'id',
                'lookup_url_kwarg': 'cart_id',
                'queryset': CartItem.objects.all(),
                'serializer_class': CartItemSerializer
            }
        }
       

class TransactionSerializer(serializers.ModelSerializer):

    model = Transaction
    fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):

    model = OrderStatus
    fields = '__all__'

       