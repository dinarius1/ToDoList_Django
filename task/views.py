from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Task, TaskRequest #TaskPermission
from .serializers import TaskSerializer, TaskRequestSerializer, RespondTaskRequestSerializer
#TaskPermissionSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor, ListCreatePermissionTask
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


# IsTaskCreatorOrReadOnly, HasTaskPermission

User = get_user_model()


"""
Проверила, все гуд
"""
class TaskListCreate(generics.ListCreateAPIView,):
    permission_classes = [IsAuthenticated,]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        print(f'{self.request.user}')

        # Возвращает список запросов на основе текущего пользователя
        return Task.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        # Устанавливает текущего пользователя как отправителя запроса
        serializer.save(creator=self.request.user)

"""
Проверила, все гуд
"""
class TaskDetail(generics.RetrieveUpdateDestroyAPIView, ListCreatePermissionTask):
    permission_classes = [IsAuthenticated, ListCreatePermissionTask]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


"""
Проверила, все гуд
Создаем и видим список запросов тасков отправителя
"""
class RequestTaskListCreateView(generics.ListCreateAPIView):
    queryset = TaskRequest.objects.all()
    serializer_class = TaskRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f'{self.request.user}')
        # Возвращает список запросов на основе текущего пользователя
        return TaskRequest.objects.filter(sender=self.request.user)

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
class RequestTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskRequest.objects.all()
    serializer_class = TaskRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f'{self.request.user}')
        # Возвращает список запросов на основе текущего пользователя
        return TaskRequest.objects.filter(sender=self.request.user)

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


class RespondTaskRequestView(APIView):

    @swagger_auto_schema(request_body=RespondTaskRequestSerializer())
    def post(self, request, pk):
        # Получение объекта TaskRequest
        task_request = get_object_or_404(TaskRequest, id=pk)

        # Создание сериализатора и передача контекста
        serializer = RespondTaskRequestSerializer(data=request.data,
                                                  context={'request': request, 'task_request': task_request})

        if serializer.is_valid():
            action = serializer.validated_data['action']

            # Обработка действия
            if action == 'accept':
                # Получаем объекты пользователей
                sender = User.objects.get(id=task_request.sender_id)
                receiver = request.user

                # Пример добавления пользователей в списки друзей (если применимо)
                # receiver_friend_list, created = FriendList.objects.get_or_create(user=receiver)
                # receiver_friend_list.friends.add(sender)
                # sender_friend_list, created = FriendList.objects.get_or_create(user=sender)
                # sender_friend_list.friends.add(receiver)

                # Помечаем запрос как неактивный
                task_request.is_active = False
                task_request.save()

                return Response({"detail": "Запрос на задачу принят."}, status=status.HTTP_200_OK)

            elif action == 'decline':
                # Помечаем запрос как неактивный
                task_request.is_active = False
                task_request.save()

                return Response({"detail": "Запрос на задачу отклонен и был удален."}, status=status.HTTP_204_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceivedTaskRequestsListView(generics.ListAPIView):
    serializer_class = TaskRequestSerializer

    def get_queryset(self):
        return TaskRequest.objects.filter(receiver=self.request.user.email,)

class RetrieveTaskRequestView(generics.RetrieveAPIView):
    serializer_class = TaskRequestSerializer

    def get_object(self):
        request_id = self.kwargs.get('request_id')
        try:
            # Возвращает запрос на дружбу по его идентификатору
            return TaskRequest.objects.get(id=request_id, receiver=self.request.user)
        except TaskRequest.DoesNotExist:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

# class ListFriendsView(generics.ListAPIView):
#     serializer_class = FriendSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return FriendList.objects.filter(user=self.request.user)




#
#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)
#
#     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
#     def add_permission(self, request, pk=None):
#         task = self.get_object()
#         if task.creator != request.user:
#             return Response(status=status.HTTP_403_FORBIDDEN)
#
#         user_email = request.data.get('user_email')
#         permission = request.data.get('permission')
#         if not user_email or not permission:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             user = User.objects.get(email=user_email)
#             TaskPermission.objects.create(task=task, user=user, permission=permission)
#             return Response(status=status.HTTP_201_CREATED)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
#     def remove_permission(self, request, pk=None):
#         task = self.get_object()
#         if task.creator != request.user:
#             return Response(status=status.HTTP_403_FORBIDDEN)
#
#         user_email = request.data.get('user_email')
#         if not user_email:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             user = User.objects.get(email=user_email)
#             permission = TaskPermission.objects.get(task=task, user=user)
#             permission.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except (User.DoesNotExist, TaskPermission.DoesNotExist):
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#
# class TaskPermissionViewSet(viewsets.ModelViewSet):
#     queryset = TaskPermission.objects.all()
#     serializer_class = TaskPermissionSerializer
#     permission_classes = [permissions.IsAuthenticated, HasTaskPermission]
#
#     def get_queryset(self):
#         task_id = self.kwargs.get('task_id')
#         return TaskPermission.objects.filter(task_id=task_id)
