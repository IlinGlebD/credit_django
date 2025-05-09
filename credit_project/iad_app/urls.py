from django.urls import path
from .views import credit_view, history_view

urlpatterns = [
    path('', credit_view, name='credit_form'),
    path('history/', history_view, name='credit_history'),
]
