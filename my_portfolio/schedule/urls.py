from django.urls import path
from . import views

app_name = "schedule"
urlpatterns = [
    path('', views.index, name='index'),
    path("add/", views.add_event, name="add_event"),
    path("remove/", views.remove_event, name="remove_event"),
    path("edit/", views.edit_event, name="edit_event"),
    path("list/", views.get_events, name="get_events"),
]