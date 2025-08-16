from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone', 
            'first_name', 'last_name',
            'gender', 'birthdate',
            'firebase_uid'
        ]
        read_only_fields = ['firebase_uid']