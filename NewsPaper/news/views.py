import logging
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, Category, Author, PostCategory
from .filters import PostFilter
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from .signals import receiver
from django.db import transaction
from django.dispatch import Signal

@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.user in category.subscribers.all():
        category.subscribers.remove(request.user)
    else:
        category.subscribers.add(request.user)

    return redirect('news_list')  # Перенаправление на страницу поста  # Если постов нет, перенаправляем на нужную страницу


def notify_subscribers(post):
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


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'news/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsList(ListView):
    model = Post
    ordering = '-some_datetime'
    template_name = "posts.html"
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.object.category.all()  # Передаем категории поста в контекст
        return context


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def form_valid(self, form):
        from .signals import post_created
        # Получаем выбранные категории
        categories_ids = self.request.POST.getlist('category')
        categories = Category.objects.filter(id__in=categories_ids)

        # Сначала сохраняем пост
        post = form.save(commit=False)
        post.author = Author.objects.get(user=self.request.user)
        post.save()  # Сохраняем пост

        # Связываем категории
        post.category.set(categories)
        post_created.send(sender=self.__class__, instance=post, created=True)

        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    login_url = '/accounts/login/'


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    login_url = '/accounts/login/'


class NewsSearchView(View):
    template_name = 'post_search.html'

    def get(self, request, *args, **kwargs):
        title = request.GET.get('title', '')
        category_id = request.GET.get('category', '')
        some_datetime = request.GET.get('some_datetime', '')

        posts = Post.objects.all()
        # Логика фильтрации постов по заголовку, категории и дате, если нужно
        if title:
            posts = posts.filter(title__icontains=title)
        if category_id:
            posts = posts.filter(category__id=category_id)

        context = {'posts': posts}
        return render(request, self.template_name, context)
