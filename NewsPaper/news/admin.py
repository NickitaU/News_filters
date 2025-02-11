from django.contrib import admin
from .models import Post, PostCategory, Category


admin.site.register(PostCategory)
admin.site.register(Post)
admin.site.register(Category)
