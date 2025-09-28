from django.urls import path
from .views import profiles_view, profile_detail

urlpatterns = [
    path('profiles/', profiles_view, name='profiles'),
    path('profiles/<int:pk>/', profile_detail, name='profile_detail'),
]
