from django.urls import path
from . import views

app_name = "tokenizer"
urlpatterns = [
    #viewsからindexを読み込んで、nameをindexに
    path("", views.tokenizer_form, name='tokenizer'),
    path("", views.add_index, name="add_index"),
]