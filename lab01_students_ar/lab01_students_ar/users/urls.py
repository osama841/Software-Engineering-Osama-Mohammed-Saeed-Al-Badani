from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .views import CustomLoginView

app_name = 'users'

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('profile/', views.profile, name='profile'),
]