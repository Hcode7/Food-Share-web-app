from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('channel/<str:username>/', views.channel, name='channel')

]