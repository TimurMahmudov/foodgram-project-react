from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    """
    Подписки
    """
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='subscribe')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Подписчик',
                             related_name='subscriber')

    class Meta:
        ordering = ('author', )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
