from django.urls import path
from . import views

app_name = 'imageblog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('image_upload', views.image_upload, name='image_upload'),
    path('preview/<int:image_id>/', views.preview, name='preview'),
    path('uploadimage_list', views.ImageListView.as_view(), name='uploadimage_list'),
    path('image_delete/<int:pk>/', views.ImageDeleteView.as_view(), name='image_delete'),
]