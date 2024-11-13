from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('get_all_users/', views.get_all_users, name='get_all_users'),
    path('reset_user_password/',views.reset_user_password, name='reset_user_password'),
]