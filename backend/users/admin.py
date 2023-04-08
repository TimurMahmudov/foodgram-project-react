from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class Subscription(admin.ModelAdmin):
    list_display = ['user', 'author']
    list_filter = ('author', )
