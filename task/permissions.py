from rest_framework.permissions import BasePermission
from user.models import User
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly, IsAdminUser, DjangoModelPermissions

class IsAuthor(BasePermission): #проверяем может ли юзер изменить/удалить комментарии
    def has_object_permission(self, request, view, obj):
    #проверяем есть ли право у юзера на изменения объекта. пишем когда работаем с конкретным объектом
        print(f'{request.user} aaaaaaaaaa')

        print(f'{obj.creator} mmmmmmmm')

        # user_obj = User.objects.get(=obj.creator)

        print(f'{obj.creator} ббббббббб')
        return request.user == obj.creator


class ListCreatePermissionTask(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        print(f'{request.method} request.method')  # Выводит текущего пользователя
        print(f'{obj.contributors.all()} obj.contributors')  # Выводит всех участников задачи

        if request.method in SAFE_METHODS or request.method == 'PUT' or  request.method == 'PATCH':
            print('SAFE_METHODS detected')  # Выводит, если метод безопасный
            if request.user in obj.contributors.all():
                print('User is in contributors')  # Выводит, если пользователь является участником
                return True

        return obj.creator == request.user  # Проверяет, является ли пользователь создателем

#from rest_framework import permissions
# from .models import TaskPermission
#
# from rest_framework import permissions
#
#
# class IsTaskCreatorOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # Доступ только для чтения разрешен всем, остальное только создателю
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.creator == request.user
#
#
# class HasTaskPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         task_id = view.kwargs.get('task_id')
#         if not task_id:
#             return False
#
#         try:
#             permission = TaskPermission.objects.get(task_id=task_id, user=request.user)
#             if view.action == 'retrieve':
#                 return permission.permission in ['read', 'update']
#             elif view.action in ['update', 'partial_update']:
#                 return permission.permission == 'update'
#         except TaskPermission.DoesNotExist:
#             return False
#
#         return False
