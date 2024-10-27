# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('simple-json/', views.simple_json_view, name='simple_json_view'),
]
