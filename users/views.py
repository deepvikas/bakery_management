from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
import jwt, datetime

from django.shortcuts import render
from .serializers import UserSerializer
from .models import BakeryUser


import logging
_logger = logging.getLogger(__name__)

# Create your views here.

class Authenticate():
    def check_authentication(self, request):
        response = {
            'status': True,
            'message': 'Authentication Required',
        }
        token = request.COOKIES.get('jwt')
        if not token:
            response['status'] = False
            response['message'] = 'Authentication Required'
            return response
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            response['status'] = False
            response['message'] = 'Authentication Required'
            return response
        response['result'] = payload
        return response

    def check_admin(self, user):
        response = {
            'status': True,
            'message': 'Success'
        }
        if user.user_type != 'admin':
            response['status'] = False
            response['message'] = 'Access Denied ! Un Authorised Operation'
        return response

class SignupView(APIView):

    def post(self, request):
        response = {
            'status': True,
            'message': 'Successfully Signup !',
            'login_ur': '/login'
        }
        serializer = UserSerializer(data=request.data)
        _logger.error("{}".format(serializer))
        if request.data['user_type'] == 'admin':
            admin = BakeryUser.objects.filter(user_type='admin')
            if admin:
                response['status'] = False
                response['message'] = 'Admin already exist !, Please Login'
                return Response(response)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(response)


class LoginView(APIView):

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        user = BakeryUser.objects.filter(username=username).first()
        if not user :
            return Response({'message': 'Incorrect Username !'})
        if not user.password == password:
            return Response({'message': 'Incorrect password !'})

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'status': True,
            'message': 'Login Successfull for {}'.format(user.username)
        }
        return response

class LogoutView(APIView):

    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'status': True,
            'message': 'Logout successfully !'
        }
        return response

class ShowUsersView(APIView):
    
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

        member_ids = BakeryUser.objects.all()
        res = []
        for member in member_ids:
            if member.user_type == 'admin':
                continue
            profile_serializer = UserSerializer(member)
            res.append(profile_serializer.data)
        return Response({
            'Members':res
        })


class DeleteUserView(APIView):
     def post(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res)
        payload = res.get('result')
        user = BakeryUser.objects.filter(id=payload['id']).first()
        res_access = auth.check_admin(user)
        try:
            if request.data['username'] != user.username and not res_access.get('status'):
                return Response(res_access)
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Something Went Wrong {}'.format(e)
            })
        user_id = BakeryUser.objects.filter(username=request.data['username']).first()
        user_id.delete()
        return Response(
            {'message': 'User Deleted Successfully', 'status': False}
        )