from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime


class NewsList(ListView):
    model = Post
    ordering = '-some_datetime'
    # queryset = Post.objects.filter(positions='PN')
    template_name = "posts.html"
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['info'] = None
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'