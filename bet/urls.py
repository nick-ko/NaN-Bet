from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login',views.login, name='login'),
    path('register',views.signin, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profil', views.profil, name='profil'),
    path('account', views.account, name='account')
]