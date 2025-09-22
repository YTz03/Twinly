from django.urls import path
from .views import questions_view

urlpatterns = [
    path('questions/', questions_view, name='questions'),
]
