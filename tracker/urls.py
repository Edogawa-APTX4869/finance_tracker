from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.homeAlert, name='homeAlert'),
    path('signin/', views.signin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signOut/', views.signOut, name='signOut'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get_expenses/', views.get_expenses, name='get_expenses'),
    path('get_incomes/', views.get_incomes, name='get_incomes'),
    path('get_weekly_balance/', views.get_weekly_balance, name='get_weekly_balance'),  # New endpoint

]