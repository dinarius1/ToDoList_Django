from django.contrib.auth import get_user_model
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import RetrievePermissionTask, UpdatePermissionTask, IsAuthor
from rest_framework import generics

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

class TaskRetrieveView(generics.RetrieveAPIView, RetrievePermissionTask):
    permission_classes = [IsAuthenticated, RetrievePermissionTask]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateView(generics.UpdateAPIView, UpdatePermissionTask):
    permission_classes = [IsAuthenticated, UpdatePermissionTask]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDestroyView(generics.DestroyAPIView, IsAuthor):
    permission_classes = [IsAuthenticated, IsAuthor]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

