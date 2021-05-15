from django.urls import path
from .api import collect_data, get_similar_cities

urlpatterns = [
    path('collect', collect_data, name='collect_data'),
    path('similar', get_similar_cities, name='get_similar_cities'),
]