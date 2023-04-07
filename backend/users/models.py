from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    """Подписки"""
    subscriber = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   verbose_name='Подписчик',
                                   related_name='subscriber')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='subscrib')

    class Meta:
        ordering = ('author', )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='unique_following'
            )
        ]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.author}'
