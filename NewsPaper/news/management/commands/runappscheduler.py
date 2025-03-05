import logging

from django.conf import settings
from news.models import Post, Category, Author, PostCategory
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    one_week_ago = timezone.now() - timedelta(minutes=1)
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()
        if subscribers.exists():
            new_posts = Post.objects.filter(category=category, some_datetime__gte=one_week_ago)
            if new_posts.exists():
                message = f"Здравствуйте!\n\nВот новые статьи из категории '{category.name_category}' за последнюю неделю:\n"
                for post in new_posts:
                    message += f"- {post.title}: {post.get_absolute_url()}\n"

                for user in subscribers:
                    send_mail(
                        subject=f"Новые статьи в категории '{category.name_category}'",
                        message=message,
                        from_email='n.ujegov@yandex.ru',
                        recipient_list=[user.email],
                    )


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")