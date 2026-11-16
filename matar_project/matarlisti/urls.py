from django.urls import path
from . import views

urlpatterns = [
    path('matarlisti/', views.matarlisti, name='matarlisti'),
    path('userlist/', views.UserList, name='userlist')
]