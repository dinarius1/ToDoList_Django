from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import FriendRequest #FriendList
from .serializers import FriendRequestSerializer, RespondFriendRequestSerializer #FriendSerializer
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model

User = get_user_model()


class SendFriendRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    @swagger_auto_schema(request_body=FriendRequestSerializer)
    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            receiver_email = serializer.validated_data['receiver']
            try:
                receiver_user = User.objects.get(email=receiver_email)
            except User.DoesNotExist:
                return Response({"detail": "Receiver user does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Проверка на существование запроса от этого отправителя к этому получателю
            if FriendRequest.objects.filter(sender=request.user, receiver=receiver_user).exists():
                return Response({"detail": "Friend request already exists."}, status=status.HTTP_200_OK)

            # Создаем запрос на дружбу
            FriendRequest.objects.create(sender=request.user, receiver=receiver_user, is_active=True)

            return Response({"detail": "Friend request sent."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RespondFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RespondFriendRequestSerializer())
    def post(self, request, request_id):
        serializer = RespondFriendRequestSerializer(data=request.data)
        print(vars(serializer))
        friend_request = FriendRequest.objects.get(id=request_id)
        print(vars(friend_request))

        if serializer.is_valid():
            if friend_request.is_active == False:
                return Response({"detail": "Запрос уже недействителен."}, status=status.HTTP_403_FORBIDDEN)

            try:
                pass
            except FriendRequest.DoesNotExist:
                return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

            if action == 'accept':
                if friend_request.sender == request.user:
                    return Response({"detail": "You cannot accept this friend request."}, status=status.HTTP_403_FORBIDDEN)

                # Получаем объекты пользователей
                sender_id = friend_request.sender_id

                receiver_email = request.user
                # print(f'{sender_id} sender_id')
                # print(f'{request.user} request.user')
                sender = User.objects.get(id=sender_id)

                receiver = User.objects.get(email=receiver_email)

                print(f'{sender} sender')
                print(f'{receiver} receiver')


                # Получаем или создаем список друзей для получателя
                # receiver_friend_list, created = FriendList.objects.get_or_create(user=receiver)
                # # Добавляем отправителя в список друзей получателя
                # receiver_friend_list.friends.add(sender)
                #
                #
                # # Получаем или создаем список друзей для отправителя
                # sender_friend_list, created = FriendList.objects.get_or_create(user=sender)
                # # Добавляем получателя в список друзей отправителя
                # sender_friend_list.friends.add(receiver)


                # Помечаем запрос как неактивный
                friend_request.is_active = False
                print(4)
                friend_request.save()

                return Response({"detail": "Friend request accepted."}, status=status.HTTP_200_OK)

            elif action == 'decline':
                # Помечаем запрос как неактивный
                friend_request.is_active = False
                friend_request.save()

                return Response({"detail": "Friend request declined."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(receiver=self.request.user.email,)

class RetrieveFriendRequestView(generics.RetrieveAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        request_id = self.kwargs.get('request_id')
        try:
            # Возвращает запрос на дружбу по его идентификатору
            return FriendRequest.objects.get(id=request_id, receiver=self.request.user)
        except FriendRequest.DoesNotExist:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

# class ListFriendsView(generics.ListAPIView):
#     serializer_class = FriendSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return FriendList.objects.filter(user=self.request.user)
