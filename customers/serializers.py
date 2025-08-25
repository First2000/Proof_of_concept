from rest_framework import serializers 
from .model import Customers 

class CustomerSerializers (serializers.ModelSerializer):
    class Meta :
        model = Customers
        field = ['id', 'name', 'revenue', 'created_at']