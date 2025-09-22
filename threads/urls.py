from django.urls import path
from .views import threads_view

urlpatterns = [
    path('threads/', threads_view, name='threads'),
]
