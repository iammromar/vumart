import string
import random
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import permissions, serializers,status, viewsets, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.api.serializers import *
from product.models import Product
User = get_user_model()

class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [AllowAny,]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        return queryset

class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [AllowAny,]

    def get_queryset(self):
        queryset = Category.objects.filter(is_active=True, parent=None)
        return queryset



class LargeResultsSetPagination(PageNumberPagination):
    page_size = 18
    page_size_query_param = 'page_size'
    max_page_size = 30


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [AllowAny,]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        cat = self.request.query_params.get('cat')
        category = Category.objects.get(pk=int(cat))
        queryset = category.products.all().filter(is_active=True)
        return queryset


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CategoryRetrieveSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [AllowAny,]
    queryset = Category.objects.all()




