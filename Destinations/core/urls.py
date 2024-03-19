from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('sessions/new', views.login, name='login'),
    path('users/new', views.signup, name='signup'),
    path('destinations', views.destinations, name='destinations'),
    path('sessions/destroy', views.logout, name='logout'),
    path('destinations/new', views.add_destination, name='add_destination'),
    path('destinations/edit/<int:destination_id>/', views.edit_destination, name='edit_destination'),
    path('destinations/delete/<int:destination_id>/', views.delete_destination, name='delete_destination'),
]