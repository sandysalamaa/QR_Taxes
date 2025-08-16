from rest_framework import serializers
from .models import Category, Receipt, Item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id', 'name', 'quantity', 'unit_price', 
            'discount', 'total_price', 'category',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ReceiptSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Receipt
        fields = [
            'id', 'merchant_name', 'total_price', 
            'discount', 'tax', 'scan_date', 'image',
            'user', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'scan_date', 'created_at', 'updated_at',
            'user'  # Typically set from request, not user input
        ]