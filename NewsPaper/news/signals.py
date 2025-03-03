from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Category
from .views import notify_subscribers
from django.db.models.signals import Signal

post_created = Signal()


@receiver(post_created)
def notify_subscribers_on_post_create(instance, created, **kwargs):
    if created:
        print("Сигнал сработал, пост создан!")  # Добавлено для отладки
        notify_subscribers(instance)
