from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:team_name>', views.thanks, name='thanks'),
]