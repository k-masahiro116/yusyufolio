from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.redirect_view, name='redirect_index'),
    path('post_list', views.PostListView.as_view(), name='post_list'),
    path('post_sidebar', views.PostSidebarView.as_view(), name='post_sidebar'),
    path('post_create', views.PostCreateView.as_view(), name='post_create'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), 
    path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'), 
    path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
]