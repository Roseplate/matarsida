from django.urls import path
from . import views

urlpatterns = [
    path('', views.default, name="default"),
    path('matarlisti/', views.matarlisti, name='matarlisti'),
    path('userlist/', views.userlist, name='userlist'),
    path('restaurantlist/', views.restaurantlist, name='restaurantlist'),
    path('restaurant/<int:stad_id>/upload/', views.upload_image, name='upload_image'),

]