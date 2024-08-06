from rest_framework import serializers
from .models import Task
from friend.models import FriendUser
from friend.serializers import FriendsSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')

    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance : Task):
        rep = super().to_representation(instance)
        user = instance.creator
        filtered_friends = FriendUser.objects.filter(task_id=instance, user=user)
        rep['friend_task'] = FriendsSerializer(filtered_friends, many=True,context=self.context).data
        return rep