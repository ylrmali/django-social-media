from django.urls import path
from accountapplication import views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('<str:user_id>/', views.profile, name='profile'),
    path('<str:username>/follower/', views.get_follower, name='get-follower'),
    path('<str:username>/following/', views.get_following, name='get-following'),
]
