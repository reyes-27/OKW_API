from django.shortcuts import render
from typing import TypeVar
from django.contrib.auth import get_user_model, login, logout
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import CustomerSerializer, CustomUserCreateSerializer, LoginUserSerializer
from .models import Customer
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.http import Http404

# Create your views here.

class CSRFApiView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        get_token(request)
        return Response(data='OK')
class RegisterView(APIView):
    permission_classes=[AllowAny,]
    def post(self, request, *args, **kwargs):
        serializer = CustomUserCreateSerializer(data=request.data)

        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response('User created successfully', status=status.HTTP_201_CREATED)
        return Response('There was an error', status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        return Response("hola")
class LoginView(APIView):
    permission_classes=[AllowAny,]
    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            print(f"DEBUG LOGIN: User {request.user} is authenticated: {request.user.is_authenticated}")
            print(f"DEBUG SESSION: {request.session.session_key}")
            return Response(data='OK', status=status.HTTP_200_OK)
        print("--- SESSION DEBUG ---")
        print(f"Request User: {request.user}")
        print(f"Session Key: {request.session.session_key}")
        print(f"Cookies received: {request.COOKIES}")
        print(f"Meta Host: {request.META.get('HTTP_HOST')}")
        return Response(data=serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileDetailView(APIView):
    permission_classes = [AllowAny,]
    def get_object(self, customer_id):
        try:
            obj = Customer.objects.get(id=customer_id)
            return obj
        except:
            raise Http404("Customer does not exist")
    def get(self, request, *args, **kwargs):
        customer = self.get_object(kwargs["id"])
        serializer = CustomerSerializer(customer)
        return Response(data={"customer":serializer.data}, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        customer = self.get_object(kwargs["id"])
        serializer = CustomerSerializer(customer, partial=True, data={request.data}, context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={"data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

