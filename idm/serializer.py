from rest_framework import serializers
from .models import Product, CustomUser

class UserSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'groups',]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
