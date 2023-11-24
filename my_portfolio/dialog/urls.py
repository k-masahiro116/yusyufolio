from django.urls import path
from . import views

app_name = 'dialog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('evaluation', views.EvaluationView.as_view(), name='evaluation'), 
    path('evaluation_detail/<int:pk>/', views.EvaluationDetailView.as_view(), name='evaluation_detail'), 
    path('post_list', views.PostListView.as_view(), name='post_list'),
    path('post_create', views.PostCreateView.as_view(), name='post_create'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), 
    path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'), 
    path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
]