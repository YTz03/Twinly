from django.urls import path
from .views import matching_view

urlpatterns = [
    path('matching/', matching_view, name='matching'),
]
