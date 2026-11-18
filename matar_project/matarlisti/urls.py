from django.urls import path
from . import views

urlpatterns = [
    # Implemented
    path('', views.default, name="default"),

    path('matarlisti/', views.matarlisti, name='matarlisti'),
    path('matarlisti/<int:start>/', views.matarlisti),
    path('matarlisti/<int:start>/<int:amount>/', views.matarlisti),

    path('profile/', views.profile, name="profile"),

    # Debug/Dev?
    path('userlist/', views.userlist, name='userlist'),
    path('restaurantlist/', views.restaurantlist, name='restaurantlist'),
    path('restaurant/<int:stad_id>/upload/', views.upload_image, name='upload_image'),

    # TODO needs to be configured entirely.
    path('history/', views.default, name="history"),
]