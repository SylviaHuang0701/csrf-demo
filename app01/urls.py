from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
]