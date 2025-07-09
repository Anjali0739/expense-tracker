from django.urls import path
from .views import add_expense, view_expenses, expense_summary

urlpatterns = [
    path('add-expense/', add_expense, name='add_expense'),
    path('view-expenses/', view_expenses, name='view_expenses'),
    path('summary/', expense_summary, name='expense_summary'),
]
