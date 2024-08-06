from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string

from .utils import send_activation_code
import hashlib


# Create your models here.
class UserManager(BaseUserManager):
    use_in_magrations = True

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Введите, пожалуйста, Вашу почту! Это необходимое поле для регистрации!')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.create_activation_code()
        send_activation_code.delay(user.email, user.activation_code)
        # отправляем на почту
        # delay - позволяет переедать задачу от джанго cellary
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        if not email:
            raise ValueError('Введите, пожалуйста, Вашу почту! Это необходимое поле для регистрации!')
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        kwargs['is_active'] = True
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    # показывает, что через это поля он будет регистрировать пользователя
    REQUIRED_FIELDS = []

    objects = UserManager()  # указываем нового менеджера

    def create_activation_code(self):
        string = self.email + str(self.id)
        encode_string = string.encode()
        md5_object = hashlib.md5(encode_string)
        activation_code = md5_object.hexdigest()
        self.activation_code = activation_code
        self.save()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

