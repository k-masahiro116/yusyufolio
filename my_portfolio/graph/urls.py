from django.urls import path
from . import views

app_name = "graph"
urlpatterns = [
    #viewsからgraphを読み込んで、nameをgraphに
    # path("graph", views.graph, name="graph"),
    #viewsからplotを読み込んで、nameをplotに
    path("graph", views.plot, name="plot"),
]