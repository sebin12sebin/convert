# converter/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_conversion_type, name='select_conversion'),
    path('<str:conversion_type>/', views.converter, name='converter'),
]
