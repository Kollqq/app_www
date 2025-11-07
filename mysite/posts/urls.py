from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/search/<str:query>/', views.category_search_by_name, name='category_search'),

    path('topics/', views.topic_list, name='topic_list'),
    path('topics/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topics/search/<str:query>/', views.topic_search_by_name, name='topic_search'),

    path('', views.PostListAPIView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailAPIView.as_view(), name='post_detail'),
]
