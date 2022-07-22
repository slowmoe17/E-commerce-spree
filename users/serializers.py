from dataclasses import fields
from django.forms import EmailField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import CustomUser


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["access"] = str(refresh.access_token)
        data["refresh"] = str(refresh)

        data["username"] = self.user.username
        data["email"] = self.user.email
        data["is_verified"] = self.user.is_verified

        make_password(self.user.password)

        return data


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "password","otp", "is_verified"]

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
            username=validated_data["username"],           
            password=make_password(validated_data["password"]),
        )
        
        user.save()
        return user





  