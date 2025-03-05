from django.apps import AppConfig


class PostCreateConfig(AppConfig):
    name = 'news'

    def ready(self):
        import news.signals  # Импортируем сигнал

