from django.urls import path

from . import views

urlpatterns = [
    path('', views.generic, name='index'),
]