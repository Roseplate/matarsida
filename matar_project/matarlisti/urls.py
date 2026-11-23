from django.urls import path
from . import views

urlpatterns = [
    # Implemented
    path('', views.default, name="default"),

    path('matarlisti/', views.matarlisti, name='matarlisti'),
    path('matarlisti/<int:start>/', views.matarlisti),
    path('matarlisti/<int:start>/<int:amount>/', views.matarlisti),

    path('profile/', views.profile, name="profile"),

    path('htmx/button/', views.menubutton, name="menubutton"),

    path('htmx/remove/', views.delete, name="remove"),

    # Debug/Dev?
    path('userlist/', views.userlist, name='userlist'),
    path('restaurantlist/', views.restaurantlist, name='restaurantlist'),
    path('restaurant/<int:stad_id>/upload/', views.upload_image, name='upload_image'),
    
    # Login/sign up and that stuff
    path('register/', views.register, name='register'),
    path('register/check-username/', views.check_username, name='check_username'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # TODO needs to be configured entirely.
    path('history/', views.default, name="history"),
]