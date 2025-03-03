from django.apps import AppConfig


class PostCreateConfig(AppConfig):
    name = 'news'

    def ready(self):
        import news.signals  # Импортируем сигнал
        from .tasks import send_mails
        from .scheduler import news_scheduler
        print("started")

        news_scheduler.add_job(
            id='mail send',
            funk=send_mails,
            trigger='interval',
            seconds=10
        )
        news_scheduler.start()
