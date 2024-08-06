from rest_framework import serializers

from .models import User
from .utils import send_activation_code


class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password_confirm')

    def validate(self, attrs):  # attrs - содержит в себе словарь с данными формата json
        # ATTRS -> OrderedDict([('email', 'admin1@gmail.com'), ('phone', '996700071102'), ('password', '12345'), ('password_confirm', '12345')])
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        # ATTRS AFTER POP -> # ATTRS -> OrderedDict([('email', 'admin1@gmail.com'), ('phone', '996700071102'), ('password', '12345')])
        if pass1 != pass2:
            raise serializers.ValidationError("Пароли не совпадают!")
        return attrs

    def validate_email(self, email):
        # EMAIL  {'email': 'admin3@gmail.com'}
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
        fields = ('email', )

    def to_representation(self, instance: User):
        # self - это обекты от ProfileSerializer
        # instance - это обекты от User. Его получим после того как нам передадут аргумент
        rep = super().to_representation(instance)
        # собирает словарь из fields = ('email', 'phone', 'bio')
        return rep


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

