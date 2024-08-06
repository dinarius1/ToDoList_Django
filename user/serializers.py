from rest_framework import serializers
from .models import User
from .utils import send_activation_code


class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password_confirm')

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError("Пароли не совпадают!")
        return attrs

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с такой почтой уже существует! Перейдите, пожалуйста, во вкладку авторизации или нажмите на кнопку "Забыл пароль"!')
        return email

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code.delay(email=user.email, activation_code=user.activation_code)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        read_only_fields = ('email',)


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

