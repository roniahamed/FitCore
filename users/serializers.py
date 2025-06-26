from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework.exceptions import ValidationError
from .models import CustomUser, UsersProfile


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


class UsersProfileSerializer(serializers.ModelSerializer):
    user = CustomSerializer(read_only=True)
    img = serializers.ImageField( required=False, allow_null=True)
     
    class Meta:
        model = UsersProfile
        fields = ['id', 'user', 'img', 'age', 'weight', 'height', 'gender', 'fitness_goal']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        if not user:
            raise ValidationError('User Must be authticated!')
        profile = UsersProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance