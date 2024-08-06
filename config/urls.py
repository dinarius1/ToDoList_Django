from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="ToDoList API",
        default_version="v1",
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui("swagger")),
    path('api/v1/user/', include('user.urls')),
    # path('api/v1/friends/', include('friend.urls')),
    path('api/v1/task/', include('task.urls')),
]