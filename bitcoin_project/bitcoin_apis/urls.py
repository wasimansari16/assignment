from django.urls import path
from .views import BitCoinExchange

urlpatterns = [
    path('api/v1/quotes', BitCoinExchange.as_view()),
]