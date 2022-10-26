from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings   

app_name = "memorize"
urlpatterns = [
    #viewsからindexを読み込んで、nameをindexに
    # path("", views.add_index, name="index"),
    path("", views.add_index, name="test"),
    path("test", views.add_index, name="test"),
    path("news", views.forecast, name="news"),
    path("diary", views.diary, name="diary"),
    path("corona", views.corona, name="corona"),
    path("youtube", views.youtube, name="youtube"),
    path("research", views.research, name="research"),
]