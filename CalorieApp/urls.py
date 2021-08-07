from django.urls import path
from CalorieApp import views

urlpatterns = [
    path('',views.homePage,name='home'),
    path('register/',views.registrationPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('selectFoodPage/',views.selectFoodPage,name='selectFood'),
    path('addFoodPage/',views.addFoodPage,name='addFood'),
    path('updateFoodPage/',views.updateFood,name='updateFood'),
    path('deleteFoodPage/',views.deleteFoodPage,name='deleteFood'),
    path('profilePage/',views.profilePage,name='profile'),
]