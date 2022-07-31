from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    username = models.CharField(
        max_length=128, blank=False,
        null=False, unique=True
    )
    email = models.EmailField(
        max_length=55, unique=True,
        blank=False, verbose_name='Почта'
    )
    first_name = models.TextField(
        max_length=55, blank=True,
        verbose_name='Имя'
    )
    last_name = models.TextField(
        max_length=55, blank=True,
        verbose_name='Фамилия'
    )
    is_subscribed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique Subscribe',
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.author}'
