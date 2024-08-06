from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, status


from .serializers import RegisterUserSerializer, ProfileSerializer, LogoutSerializer

from .models import User


# Create your views here.

class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #вырабатываются все функции, которые мы прописали в сериализаторe, связанные с validate
        serializer.save()
        #при сейве вырабатывается def create(self, validated_data) из сериализатора
        return Response('Регистрация прошла успешно, но необходимо активировать аккаунт! Для этого, пожалуйста, проверьте вашу почту, мы выслали вам письмо для полной завершении регистрации.', status=201)


@api_view(["GET"])
def activate(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = ''
    user.save()

    # Создаем access и refresh токены
    refresh = RefreshToken.for_user(user)
    # Возвращаем токены в ответе
    response_data = {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }
    return Response(response_data, status=200)

class ProfileViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         serializer = LogoutSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         refresh_token = serializer.validated_data['refresh_token']
#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()  # Marks the token as no longer valid
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         return Response(status=status.HTTP_204_NO_CONTENT)