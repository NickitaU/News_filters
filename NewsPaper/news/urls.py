from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, PostCreate, PostUpdate, PostDelete, NewsSearchView

urlpatterns = [
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', NewsSearchView.as_view(), name='news_search'),

]
