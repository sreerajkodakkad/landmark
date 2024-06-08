# sales/serializers.py

from rest_framework import serializers
from .models import Sales
from django.contrib.auth.models import User


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
