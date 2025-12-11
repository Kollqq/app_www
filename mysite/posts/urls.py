from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>/topics/', views.category_topics, name='category_topics'),
    path('categories/search/<str:query>/', views.category_search_by_name, name='category_search'),
    path('categories/<int:pk>/permission-test/', views.category_permission_test),

    path('topics/', views.topic_list, name='topic_list'),
    path('topics/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('topics/search/<str:query>/', views.topic_search_by_name, name='topic_search'),

    path('', views.PostListAPIView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailAPIView.as_view(), name='post_detail'),

    path('<int:pk>/update/', views.PostUpdateAPIView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteAPIView.as_view(), name='post_delete'),

    path('users/posts/', views.user_posts, name='user_posts'),

    path("html/topics/", views.topic_list_html, name="topic_list_html"),
    path("html/topics/<int:pk>/", views.topic_detail_html, name="topic_detail_html"),

    path("html/posts/", views.post_list_html, name="post_list_html"),
    path("html/posts/<int:pk>/", views.post_detail_html, name="post_detail_html"),

    path("html/topics/<int:pk>/posts/", views.topic_posts_html, name="topic_posts_html"),
]