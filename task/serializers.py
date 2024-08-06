from rest_framework import serializers
from .models import Task, TaskRequest
from django.contrib.auth import get_user_model

User = get_user_model()
class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')

    class Meta:
        model = Task
        fields = '__all__'

class TaskRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRequest
        fields = '__all__'

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


class RespondTaskRequestSerializer(serializers.ModelSerializer):
    ACTION_CHOICES = [
        ('accept', 'Accept'),
        ('decline', 'Decline'),
    ]
    action = serializers.ChoiceField(choices=ACTION_CHOICES)
    task_request = TaskRequestSerializer(read_only=True)

    class Meta:
        model = TaskRequest
        fields = ['task_request', 'action']

    def validate(self, data):
        action = data.get('action')
        task_request = self.context['task_request']  # Передайте объект TaskRequest через контекст

        # Проверка, что запрос активен
        if not task_request.is_active:
            raise serializers.ValidationError('Запрос уже недействителен.')

        return data