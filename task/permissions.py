from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor(BasePermission):
    message = 'Вы не являетесь автором этой задачи!'

    def has_object_permission(self, request, view, obj):
        # print((f" {request.user} {obj.creator}"))
        return request.user == obj.creator


class RetrievePermissionTask(BasePermission):
    message = 'У вас нет разрешение на просмотр этой задачи!'

    def has_object_permission(self, request, view, obj):
        print(f"Request Method: {request.method}")
        print(f"Request User: {request.user}")

        if request.method in SAFE_METHODS:
            print("Safe method detected")
            for friend_user in obj.friend_task.all():

                print(f'{friend_user}')
                print(f'{friend_user.friend}')
                print(f"Friend user email: {friend_user.user.email}")
                if request.user == friend_user.friend and friend_user.right_to_read:
                    # print("User has read rights in friend_task")
                    return True
        return obj.creator == request.user
        # Проверяет является ли пользователь создателем


class UpdatePermissionTask(BasePermission):
    message = 'У вас нет разрешения на обновление этой задачи!'

    def has_object_permission(self, request, view, obj):
        print(f"Request Method: {request.method}")
        print(f"Request User: {request.user}")

        if request.method in ['PUT', 'PATCH']:
            print("Safe method detected")
            for friend_user in obj.friend_task.all():

                print(f'{friend_user}')
                print(f'{friend_user.friend}')
                print(f"Friend user email: {friend_user.user.email}")
                if request.user == friend_user.friend and friend_user.right_to_update:
                    # print("User has read rights in friend_task")
                    return True
        return obj.creator == request.user
