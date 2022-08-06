from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.NewsIndex.as_view(), name='index'),
    path('category/<tag>/', views.Category.as_view(), name='category'),
]
