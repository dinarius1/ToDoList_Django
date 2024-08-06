from rest_framework import serializers
from .models import FriendUser,FriendRequest, FriendList
from task.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'email']


class FriendUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FriendUser
        fields = ['id', 'user', 'friend', 'task_id', 'right_to_read', 'right_to_update']


class FriendListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friends = FriendUserSerializer(many=True)

    class Meta:
        model = FriendList
        fields = ['id', 'user', 'friends']


class FriendsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FriendUser
        fields = ['id', 'user', 'friend', 'task_id', 'right_to_read', 'right_to_update']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('id', 'sender', 'receiver', 'task_id', 'right_to_read', 'right_to_update', 'is_active')

    def validate(self, data):
        receiver_email = data.get('receiver')
        is_active = data.get('is_active')

        # Проверка на существование пользователя
        if not User.objects.filter(email=receiver_email).exists():
            raise serializers.ValidationError('Пользователь с такой почтой не найден!')

        # Проверка на отправку самому себе
        if self.context['request'].user.email == receiver_email:
            raise serializers.ValidationError('Нельзя отправить запрос самому себе!')

        # Проверка на активность запроса
        if not is_active:
            raise serializers.ValidationError('Запрос на задачу уже недействителен!')

        return data


class RespondFriendRequestSerializer(serializers.ModelSerializer):
    ACTION_CHOICES = [
        ('accept', 'Accept'),
        ('decline', 'Decline'),
    ]
    action = serializers.ChoiceField(choices=ACTION_CHOICES)

    class Meta:
        model = FriendRequest
        fields = ['action',]

    def validate(self, data):
        action = data.get('action')
        friend_request = self.context['friend_request']

        if not friend_request.is_active:
            raise serializers.ValidationError('Запрос уже недействителен.')
        return data


class FollowedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'deadline']


class FollowedListSerializer(serializers.ModelSerializer):
    # task_detail = FollowedTaskSerializer(many=True, read_only=True)
    friend_user = FriendUserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'friend_user']

    def to_representation(self, instance: User):
        rep = super().to_representation(instance)
        return rep

