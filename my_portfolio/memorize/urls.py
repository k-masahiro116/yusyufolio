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
    path("dialog", views.dialog, name="dialog"),
    path("portfolio", views.portfolio, name="portfolio"),
    path("corona", views.corona, name="corona"),
    path("youtube", views.youtube, name="youtube"),
    path("practice", views.practice, name="practice"),
]