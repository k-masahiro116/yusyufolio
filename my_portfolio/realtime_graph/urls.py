from django.urls import path
from . import views

app_name = "realtime_graph"
urlpatterns = [
    #viewsからgraphを読み込んで、nameをgraphに
    # path("graph", views.graph, name="graph"),
    #viewsからplotを読み込んで、nameをplotに
    path("realtime_graph", views.plot, name="plot"),
]