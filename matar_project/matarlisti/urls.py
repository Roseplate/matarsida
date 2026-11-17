from django.urls import path
from . import views

urlpatterns = [
    path('', views.default, name="default"),
    path('matarlisti/', views.matarlisti, name='matarlisti'),
    path('userlist/', views.UserList, name='userlist')
]