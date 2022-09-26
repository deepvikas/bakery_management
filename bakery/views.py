from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from users.views import Authenticate
from users.models import BakeryUser
from .models import Product
from .serializers import ProductSerializer
# Create your views here.

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
        tem = Product.objects.filter(id=request.data['id']).first()
        item.delete()
        return Response({
            'status': True,
            'message': 'Item Successfully Deleted.'
        })

class UpdateQuantity(APIView):

    def put(self, request):
        if not request.data.get('id') or not request.data.get('new_quantity'):
            return Response({
                'message': 'Required Parameter Id or new_quantity is missing.'
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
            id=request.data.get('id')
        ).first()
        if not product:
            return Response({"message": 'Product does not exist.'})
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({
            'message': 'Something Went Wrong'
        })