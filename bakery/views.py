from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from users.views import Authenticate
from users.models import BakeryUser
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
# Create your views here.

import datetime

import logging

_logger = logging.getLogger(__name__)

class AddItemsView(APIView):
    
    def post(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res)
        payload = res.get('result')

        user = BakeryUser.objects.filter(id=payload['id']).first()
        res_access = auth.check_admin(user)
        if not res_access.get('status'):
            return Response(res_access)

        product = ProductSerializer(data=request.data)
        product.is_valid(raise_exception=True)
        product.save()
        return Response(product.data)

class GetItemsView(APIView):

    def get(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res)
        payload = res.get('result')        
        user = BakeryUser.objects.filter(id=payload['id']).first()        
        res_access = auth.check_admin(user)
        if not res_access.get('status'):
            return Response(res_access)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)        
        

class DeleteItemView(APIView):

    def post(self, request):
        if not request.data.get('id'):
            return Response({
                'status': False,
                'message': 'Required id Parameter is missing in payload.'
            })
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res)
        payload = res.get('result')        
        user = BakeryUser.objects.filter(id=payload['id']).first()        
        res_access = auth.check_admin(user)
        if not res_access.get('status'):
            return Response(res_access)
        item = Product.objects.filter(id=request.data['id']).first()
        item.delete()
        return Response({
            'status': True,
            'message': 'Item Successfully Deleted.'
        })

class UpdateQuantity(APIView):

    def put(self, request):
        if not request.data.get('id') or not request.data.get('quantity'):
            return Response({
                'message': 'Required Parameter Id or quantity is missing.'
            })
        
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res)
        payload = res.get('result')        
        user = BakeryUser.objects.filter(id=payload['id']).first()        
        res_access = auth.check_admin(user)
        if not res_access.get('status'):
            return Response(res_access)
        product = Product.objects.filter(
            pk=request.data.get('id')).first()
        product.quantity = request.data.get('quantity')
        product.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class ShopDetialView(APIView):

    def get(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res)
        product = Product.objects.filter(quantity__gt=0)
        _logger.info(product)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

class CreateOrderView(APIView):

    def post(self, request):
        if not request.data.get('product_id') or not request.data.get('quantity'):
            return Response({
                'message': 'Product Id or Quantity is missing.'
            })
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res)
        payload = res.get('result')        
        user = BakeryUser.objects.filter(id=payload['id']).first()
        product = Product.objects.filter(pk=request.data.get('product_id')).first()
        total_amount = product.selling_price * int(request.data.get('quantity'))
        vals = {
            'product_id': product.id,
            'quantity': int(request.data.get('quantity')),
            'user_id': user.id,
            'amount': total_amount
        }
        order = OrderSerializer(data=vals)
        order.is_valid(raise_exception=True)
        order.save()
        response = {
            'message': 'Order Placed',
            'total_amount': total_amount
        }
        return Response(response)

class OrderHistoryView(APIView):

    def get(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res)
        payload = res.get('result')        
        history = Order.objects.filter(user_id=payload['id'])
        orders = OrderSerializer(history, many=True)
        return Response(orders.data)
        