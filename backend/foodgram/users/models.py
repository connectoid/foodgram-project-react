from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    GUEST = 'guest'
    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (GUEST, GUEST),
        (USER, USER),
        (ADMIN, ADMIN),
    ]
    login = models.CharField(max_length=128, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(max_length=55, unique=True,
                              blank=False, verbose_name='Почта')
    name = models.TextField(blank=True, verbose_name='Имя')
    fname = models.TextField(blank=True, verbose_name='Фамилия')
    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES,
                            default=USER,
                            verbose_name='Роль'
                            )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
