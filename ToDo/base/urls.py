from django.urls import path, include

from . import views

app_name = 'base'

urlpatterns = [
    path('tasks/', views.processTasks, name='task'),   
]