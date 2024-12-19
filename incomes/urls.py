from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='incomes'),
    path('add-income/', views.add_income, name='add-income'),
    path('edit-income/<int:income_id>/', views.edit_income, name='edit-income'),
    path('delete-income/<int:income_id>/', views.delete_income, name='delete-income'),
    path('get_income_sources/', views.income_sources_summary, name='get_income_sources'),
]