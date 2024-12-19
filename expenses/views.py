from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense, Category
from userpreferences.models import userPreferences
from django.http import JsonResponse
from django.core.paginator import Paginator
from decimal import Decimal
from django.db import connection
from datetime import datetime, timedelta




# Create your views here.

@login_required()
def index(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-id')
    for expense in expenses:
        expense.category_name = expense.category.name

    paginator = Paginator(expenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    currency = userPreferences.objects.get(user=request.user).currency

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }

    return render(request, 'App/Expenses/index.html', context)

@login_required
def add_expenses(request):
    if request.method == 'POST':
        category_id = request.POST.get('expenseCategory')
        amount = request.POST.get('expenseAmount')
        date = request.POST.get('expenseDate')
        description = request.POST.get('description', '')

        category = Category.objects.get(id=category_id)
        Expense.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            description=description,
            date=date
        )
        messages.success(request, 'Expense added successfully.')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': '/expenses/'})

        return redirect('expenses')

    currency = userPreferences.objects.get(user=request.user).currency
    categories = list(Category.objects.values('id', 'name'))

    context = {
        'categories': categories,
        'currency': currency
    }

    return render(request, 'App/Expenses/add-expenses.html', context)

@login_required
def edit_expenses(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    if request.method == 'POST':
        category_id = request.POST.get('expenseCategory')
        amount = request.POST.get('expenseAmount')
        date = request.POST.get('expenseDate')
        description = request.POST.get('description', '')

        category = Category.objects.get(id=category_id)
        expense.category = category
        expense.amount = amount
        expense.date = date
        expense.description = description
        expense.save()
        messages.success(request, 'Expense updated successfully.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': '/expenses/'})
        return redirect('expenses')

    categories = list(Category.objects.values('id', 'name'))
    currency = userPreferences.objects.get(user=request.user).currency
    context = {
        'expense': expense,
        'categories': categories,
        'currency': currency
    }
    return render(request, 'App/Expenses/edit-expenses.html', context)

@login_required
def delete_expenses(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    expense.delete()
    messages.success(request, 'Expense deleted successfully.')
    return redirect('expenses')

@login_required
def expense_category_summary(request):
    user = request.user
    filter_type = request.GET.get('filter', 'this_month')

    finalrep = {}
    with connection.cursor() as cursor:
        db = cursor.db_conn
        expense_collection = db['expenses_expense']

        db = cursor.db_conn
        income_collection = db['incomes_income']

        if filter_type == 'this_month':
            start_date = datetime(datetime.now().year, datetime.now().month, 1)
        elif filter_type == 'whole':
            start_date = datetime.min
        elif filter_type == '30_days':
            start_date = datetime.now() - timedelta(days=30)
        elif filter_type == '7_days':
            start_date = datetime.now() - timedelta(days=7)
        elif filter_type == 'today':
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            start_date = datetime(datetime.now().year, datetime.now().month, 1)

        expenses_cursor = expense_collection.find({
            'user_id': user.id,
            'date': {'$gte': start_date}
        })

        # Calculate totals by category
        category_totals = {}
        for expense in expenses_cursor:
            category = expense['category_id']
            amount = Decimal(expense['amount'].to_decimal())
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount

    categories = {str(category.id): category.name for category in Category.objects.all()}
    x_values = [categories.get(str(category_id), "Unknown") for category_id in category_totals.keys()]
    y_values = [float(total) for total in category_totals.values()]

    return JsonResponse({'xValues': x_values, 'yValues': y_values})