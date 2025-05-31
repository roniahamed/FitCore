from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework.exceptions import ValidationError
from .models import CustomUser


class CustomSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def get_cleaned_data(self,):
        return {
            'email': self.validated_data.get('email', ''),
            'password':self.validated_data.get('password1', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name' : self.validated_data.get('last_name')
        }

    def save(self, request):
        cleaned_data = self.get_cleaned_data()
        if CustomUser.objects.filter(email = cleaned_data['email']).exists():
            raise ValidationError('This email is already register')
        user = CustomUser(
            email = cleaned_data['email'],
            first_name = cleaned_data['first_name'],
            last_name = cleaned_data['last_name']
        )
        user.set_password(cleaned_data['password'])
        user.save()
        return user


class RegisterSerializer(serializers.ModelSerializer):
    username = None
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, label="Confirm Password")
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name','password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Your passwords didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user 
    

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']

    def update(self, instance, validate_data):
        for attr, value in validate_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance