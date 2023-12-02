import imp
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from product.models import *
User = get_user_model()

class ParentCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
class CategoryListSerializer(serializers.ModelSerializer):
    parent = ParentCategoryListSerializer()
    children = SubCategoryListSerializer(many=True)
    class Meta:
        model = Category
        fields = "__all__"




class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"

class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    main_image = serializers.SerializerMethodField()
    category = CategoryListSerializer(many=True)
    
    def get_main_image(self, product, *args, **kwargs):
        image = product.images.filter(is_main=True).last()
        if image:
            return str(image.image)
        else:
            return None


    class Meta:
        model = Product
        fields = ['id', 'main_image','images', 'price','discount_price','short_description','description','name','category']




class CategoryRetrieveSerializer(serializers.ModelSerializer):
    parent = ParentCategoryListSerializer()
    children = SubCategoryListSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"