from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import FriendUser, FriendRequest, FriendList
from .serializers import FriendRequestSerializer, RespondFriendRequestSerializer, FriendUserSerializer, FriendListSerializer, FollowedListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

"""
Проверила, все гуд
Создаем и видим список запросов тасков отправителя
"""

User = get_user_model()


class RequestFriendListCreateView(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f'{self.request.user}')
        # Возвращает список запросов на основе текущего пользователя
        return FriendRequest.objects.filter(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        # Получение сериализатора с данными запроса
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Если данные валидны, вызываем метод create
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Сохранение объекта с текущим пользователем в качестве отправителя
        serializer.save(sender=self.request.user)

"""
Проверила, все гуд
Обноваление, удаление, чтение детальное 1 запроса таска отправителя
"""


class RequestFriendRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f'{self.request.user}')
        # Возвращает список запросов на основе текущего пользователя
        return FriendRequest.objects.filter(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        # Получение сериализатора с данными запроса
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Если данные валидны, вызываем метод create
        return super().create(request, *args, **kwargs)

    def perform_update(self, serializer):
        # Сохранение объекта с текущим пользователем в качестве отправителя
        serializer.save(sender=self.request.user)


class RespondFriendRequestView(APIView):
    @swagger_auto_schema(request_body=RespondFriendRequestSerializer())
    def post(self, request, pk):
        friend_request = get_object_or_404(FriendRequest, id=pk)
        serializer = RespondFriendRequestSerializer(data=request.data, context={'request': request, 'friend_request': friend_request})

        if serializer.is_valid():
            action = serializer.validated_data['action']
            right_to_read = friend_request.right_to_read
            right_to_update = friend_request.right_to_update

            # Обработка действия
            if action == 'accept':
                sender = User.objects.get(id=friend_request.sender_id)
                receiver = request.user

                sender_to_receiver, created = FriendUser.objects.get_or_create(
                    friend=receiver,
                    user=sender,
                    task_id=friend_request.task_id,
                    right_to_read=right_to_read,
                    right_to_update=right_to_update
                )

                sender_friend_list, created = FriendList.objects.get_or_create(user=sender)
                sender_friend_list.friends.add(sender_to_receiver)

                # Помечаем запрос как неактивный
                friend_request.is_active = False
                friend_request.save()

                return Response({"detail": "Запрос на дружбу принят."}, status=status.HTTP_200_OK)

            elif action == 'decline':
                # Помечаем запрос как неактивный
                friend_request.is_active = False
                friend_request.save()

                return Response({"detail": "Запрос на дружбу отклонен и был удален."}, status=status.HTTP_204_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceivedFriendRequestsListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(receiver=self.request.user.email,)

class RetrieveFriendRequestView(generics.RetrieveAPIView):
    serializer_class = FriendRequestSerializer

    def get_object(self):
        request_id = self.kwargs.get('request_id')
        try:
            # Возвращает запрос на дружбу по его идентификатору
            return FriendRequest.objects.get(id=request_id, receiver=self.request.user)
        except FriendRequest.DoesNotExist:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)


class FriendListView(generics.ListAPIView):
    serializer_class = FriendListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendList.objects.filter(user=self.request.user)


class FriendUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FriendUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendUser.objects.filter(user=self.request.user)


class FollowedTaskListView(generics.ListAPIView):
    serializer_class = FollowedListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(friend_user__friend=user).distinct()
