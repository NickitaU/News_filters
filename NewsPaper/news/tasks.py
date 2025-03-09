from celery import shared_task
from django.core.mail import send_mail
from celery import shared_task
from .models import Post, Category
from django.utils import timezone
from datetime import timedelta



@shared_task
def notify_subscribers_task(post_id):
    from .models import Post  # Импортируем модель здесь, чтобы избежать циклических зависимостей
    post = Post.objects.get(id=post_id)

    for category in post.category.all():
        for user in category.subscribers.all():
            try:
                send_mail(
                    subject=post.title,
                    message=f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!\n{post.text}...",
                    from_email='n.ujegov@yandex.ru',
                    recipient_list=[user.email],
                )
            except Exception as e:
                print(f"Ошибка при отправке сообщения {user.email}: {e}")


@shared_task
def send_weekly_newsletters():
    one_week_ago = timezone.now() - timedelta(days=7)
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
