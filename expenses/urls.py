from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expenses/', views.add_expenses, name='add-expenses'),
    path('edit-expenses/<int:expense_id>/', views.edit_expenses, name='edit-expenses'),
    path('delete-expenses/<int:expense_id>/', views.delete_expenses, name='delete-expenses'),
    path('get_category_expenses/', views.expense_category_summary, name='get_category_expenses'),
]