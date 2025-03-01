from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, PostCreate, PostUpdate, PostDelete, NewsSearchView
from .views import IndexView
from .views import subscribe_to_category

urlpatterns = [
    path('', IndexView.as_view()),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', NewsSearchView.as_view(), name='news_search'),
    path('subscribe/<int:category_id>/', subscribe_to_category, name='subscribe_to_category'),
]

