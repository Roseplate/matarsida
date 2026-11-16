from django.urls import path
from . import views

urlpatterns = [
    path('matarlisti/', views.matarlisti, name='matarlisti'),
    path('userlist/', views.userlist, name='userlist'),
    path('restaurantlist/', views.restaurantlist, name='restaurantlist')
]