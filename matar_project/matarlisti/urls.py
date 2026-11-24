from django.urls import path
from . import views

urlpatterns = [
    # Implemented (Stuff that has been linked to a page and is meant to be seen, even if the page is not finished)
    path('', views.default, name="default"),

    path('matarlisti/', views.matarlisti, name='matarlisti'),
    path('matarlisti/<int:start>/', views.matarlisti),
    path('matarlisti/<int:start>/<int:amount>/', views.matarlisti),

    path('profile/', views.profile, name="profile"),

    path('history/', views.history, name="history"),

    # Login/sign up and that stuff
    path('register/', views.register, name='register'),
    path('register/check-username/', views.check_username, name='check_username'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('htmx/button/', views.menubutton, name="menubutton"),
    path('htmx/remove/', views.delete, name="remove"),

    # Debug/Dev, (stuff not meant to be seen, remove before publishing)
    path('userlist/', views.userlist, name='userlist'),
    path('restaurantlist/', views.restaurantlist, name='restaurantlist'),
    path('restaurant/<int:stad_id>/upload/', views.upload_image, name='upload_image'),
    
    # TODO needs to be configured entirely.
]