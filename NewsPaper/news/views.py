from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post,Category
from .filters import PostFilter
from datetime import datetime
from django.shortcuts import render
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from datetime import datetime
from django.utils import timezone


class NewsList(ListView):
    model = Post
    ordering = '-some_datetime'
    # queryset = Post.objects.filter(positions='PN')
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


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_eqit.html'


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_eqit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class NewsSearchView(View):
    template_name = 'post_search.html'

    def get(self, request, *args, **kwargs):
        title = request.GET.get('title', '')
        category_id = request.GET.get('category', '')
        some_datetime = request.GET.get('some_datetime', '')

        posts = Post.objects.all()

        if title:
            posts = posts.filter(title__icontains=title)
        if category_id:
            posts = posts.filter(category__id=category_id)
        if some_datetime:
            try:
                input_date = datetime.strptime(some_datetime, '%Y-%m-%d')
                posts = posts.filter(some_datetime__gt=input_date)
            except ValueError:
                pass

        categories = Category.objects.all()

        context = {
            'posts': posts,
            'categories': categories,
            'title': title,
            'category': category_id,
            'some_datetime': some_datetime,
        }

        return render(request, self.template_name, context)
