from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=128, blank=False, null=False, unique=True)
    #password = models.CharField(max_length=128, blank=False, null=False)
    email = models.EmailField(max_length=55, unique=True,
                              blank=False, verbose_name='Почта')
    first_name = models.TextField(max_length=55, blank=True, verbose_name='Имя')
    last_name = models.TextField(max_length=55, blank=True, verbose_name='Фамилия')
    is_subscribed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'password']


    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
