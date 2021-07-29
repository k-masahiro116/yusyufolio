from django.urls import path
from . import views

app_name = "function"
urlpatterns = [
    path("contact", views.contact_form, name='contact'),
    path('contact/complete', views.complete, name='complete'),
]