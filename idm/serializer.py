from rest_framework import serializers
from .models import Product, Profile


class UserSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    class Meta:
        model = Profile
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
