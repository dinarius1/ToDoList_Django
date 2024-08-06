from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskListCreate, RequestTaskListCreateView, RespondTaskRequestView, ReceivedTaskRequestsListView, RetrieveTaskRequestView, TaskDetail, RequestTaskRetrieveUpdateDestroyView
#TaskPermissionViewSet


urlpatterns = [
    # path('task_request/', SendTaskRequestView.as_view()),
    path('task_request/', RequestTaskListCreateView.as_view()),
    path('task_request/<int:pk>', RequestTaskRetrieveUpdateDestroyView.as_view()),
    path('received_task_request/', ReceivedTaskRequestsListView.as_view()),
    path('respond_task_request/<int:pk>/', RespondTaskRequestView.as_view()),
    # path('friends/', ListFriendsView.as_view(), name='list_friends'),
    path('task', TaskListCreate.as_view(), name='listcreate'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='detailcreate'),
    # path('tasks/<int:task_id>/permissions/', TaskPermissionViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('tasks/<int:task_id>/permissions/<int:pk>/', TaskPermissionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    # path('tasks/<int:pk>/add_permission/', TaskViewSet.as_view({'post': 'add_permission'}), name='add-permission'),
    # path('tasks/<int:pk>/remove_permission/', TaskViewSet.as_view({'post': 'remove_permission'}), name='remove-permission'),
]
