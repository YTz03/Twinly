from django.urls import path
from .views import matching_view, match_list

urlpatterns = [
    path('matching/', matching_view, name='matching'),
    path('matches/', match_list, name='match_list'),
]
