from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # 首页
    path('', views.home, name='home'),
    
    # 图书管理
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/update/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # 分类管理
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # 作者管理
    path('authors/', views.author_list, name='author_list'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('authors/create/', views.author_create, name='author_create'),
    path('authors/<int:pk>/update/', views.author_update, name='author_update'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),
    
    # 统计分析
    path('statistics/', views.statistics, name='statistics'),
]
