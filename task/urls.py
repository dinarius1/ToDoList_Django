from django.urls import path
from .views import TaskListCreate, TaskRetrieveView, TaskUpdateView, TaskDestroyView

urlpatterns = [
    path('task', TaskListCreate.as_view()),
    path('task/<int:pk>/', TaskRetrieveView.as_view()),
    path('task/<int:pk>/update/', TaskUpdateView.as_view()),
    path('task/<int:pk>/delete/', TaskDestroyView.as_view()),
]
