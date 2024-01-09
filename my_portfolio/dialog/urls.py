from django.urls import path
from . import views

app_name = 'dialog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('user_list', views.UserdataListView.as_view(), name='user_list'), 
    path('user_create', views.UserdataCreateView.as_view(), name='user_create'), 
    path('user_detail/<int:pk>/', views.UserdataDetailView.as_view(), name='user_detail'), 
    path('user_update/<int:pk>/', views.UserdataUpdateView.as_view(), name='user_update'), 
    path('user_delete/<int:pk>/', views.UserdataDeleteView.as_view(), name='user_delete'), 
    path('evaluation', views.EvaluationView.as_view(), name='evaluation'), 
    path('evaluation_detail/<int:pk>/', views.EvaluationDetailView.as_view(), name='evaluation_detail'), 
    path('evaluation_delete/<int:pk>/', views.EvaluationDeleteView.as_view(), name='evaluation_delete'), 
    path('evaluation_update/<int:pk>/', views.EvaluationUpdateView.as_view(), name='evaluation_update'), 
    path('post_list', views.PostListView.as_view(), name='post_list'),
    path('post_create', views.PostCreateView.as_view(), name='post_create'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), 
    path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'), 
    path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
]