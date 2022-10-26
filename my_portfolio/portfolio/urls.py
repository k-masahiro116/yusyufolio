from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings   

app_name = "portfolio"
urlpatterns = [
    #viewsからindexを読み込んで、nameをindexに
    # path("", views.add_index, name="index"),
    path("", views.add_index, name="index"),
]