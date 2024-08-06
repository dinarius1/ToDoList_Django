# from rest_framework import serializers
# from .models import FriendRequest #FriendList
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
# # class FriendSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = FriendList
# #         fields = ['user', 'friends',]
# #
# # class UserSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = User
# #         fields = ['id', 'email']
#
#
# class FriendRequestSerializer(serializers.ModelSerializer):
#     receiver = serializers.EmailField()
#
#     class Meta:
#         model = FriendRequest
#         fields = '__all__'
#
#     def validate_email(self, receiver):
#         from user.models import User
#         # EMAIL  {'email': 'admin3@gmail.com'}
#         if User.objects.filter(email=receiver).DoesNotExist():
#             raise serializers.ValidationError('Пользователь с такой почтой не существует!')
#         return receiver
#
#     def create(self, validated_data):
#         sender = self.context['request'].user
#         receiver_email = validated_data['receiver']
#         receiver = User.objects.get(email=receiver_email)
#         return FriendRequest.objects.create(sender=sender, receiver=receiver)
#
#
# class RespondFriendRequestSerializer(serializers.ModelSerializer):
#     ACTION_CHOICES = [
#         ('accept', 'Accept'),
#         ('decline', 'Decline'),
#     ]
#     action = serializers.ChoiceField(choices=ACTION_CHOICES)
#     friend_request = FriendRequestSerializer(read_only=True)
#
#     class Meta:
#         model = FriendRequest
#         fields = ['friend_request', 'action']