from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('food/<slug:slug>/', views.food_detail, name='food_detail'),
    path('recipes/', views.food_list, name='food_list'),
    path('create/', views.add_food, name='add_food'),
    path('update-food/<slug:slug>/', views.update_food, name='update_food'),
    path('delete-food/<slug:slug>/', views.delete_food, name='delete_food'),
    path('premium/', views.subscribe, name='subscription_page'),
    path('subscription/', views.premium, name='premium'),
    path('food/<slug:slug>/like/', views.like_view, name='likes'),
]