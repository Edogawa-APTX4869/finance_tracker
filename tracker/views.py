from django.db import connection
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from userpreferences.models import userPreferences
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils import timezone


def home(request):
    return render(request, 'home.html')
def homeAlert(request):
    return render(request, 'home.html', {'warning': 'You need to sign in to access the application'})
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'home.html', {'error': 'Invalid username or password'})
    return redirect('home')
def signup(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('emailAddress')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'home.html')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # add default user preferences
                user_preferences = userPreferences(user=user)
                user_preferences.save()


                login(request, user)
                return redirect('dashboard')
        else:
            return render(request, 'home.html', {'error': 'Passwords do not match'})
    return render(request, 'home.html')
def signOut(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'home.html', {'message': 'You have been logged out successfully'})
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user

    # Access MongoDB collection directly
    with connection.cursor() as cursor:
        # Get the database and collection
        db = cursor.db_conn
        income_collection = db['incomes_income']
        expense_collection = db['expenses_expense']

        # Query total incomes and expenses
        incomes_cursor = income_collection.find({'user_id': user.id})
        expenses_cursor = expense_collection.find({'user_id': user.id})

        # Sum up the amounts
        total_incomes = sum(Decimal(income['amount'].to_decimal()) for income in incomes_cursor)
        total_expenses = sum(Decimal(expense['amount'].to_decimal()) for expense in expenses_cursor)

        # Calculate expenses for this month
        start_of_month = datetime(datetime.now().year, datetime.now().month, 1)
        expenses_this_month_cursor = expense_collection.find({
            'user_id': user.id,
            'date': {'$gte': start_of_month}
        })
        expenses_this_month = sum(Decimal(expense['amount'].to_decimal()) for expense in expenses_this_month_cursor)

        # Calculate incomes for this month
        incomes_this_month_cursor = income_collection.find({
            'user_id': user.id,
            'date': {'$gte': start_of_month}
        })
        incomes_this_month = sum(Decimal(income['amount'].to_decimal()) for income in incomes_this_month_cursor)

    # Calculate the balance
    balance = total_incomes - total_expenses

    # Get user preferences
    user_pref = userPreferences.objects.get(user=user)
    currency = user_pref.currency

    # Pass data to the template
    context = {
        'total_incomes': total_incomes,
        'total_expenses': total_expenses,
        'balance': balance,
        'currency': currency,
        'expenses_this_month': expenses_this_month,
        'incomes_this_month': incomes_this_month
    }

    return render(request, 'App/dashboard.html', context)

@login_required
def get_expenses(request):
    user = request.user
    filter_type = request.GET.get('filter', 'this_month')

    # Access MongoDB collection directly
    with connection.cursor() as cursor:
        db = cursor.db_conn
        expense_collection = db['expenses_expense']

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
        expenses = sum(Decimal(expense['amount'].to_decimal()) for expense in expenses_cursor)

    return JsonResponse({'expenses': expenses})

@login_required
def get_expenses(request):
    user = request.user
    filter_type = request.GET.get('filter', 'this_month')

    # Access MongoDB collection directly
    with connection.cursor() as cursor:
        db = cursor.db_conn
        expense_collection = db['expenses_expense']

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
        expenses = sum(Decimal(expense['amount'].to_decimal()) for expense in expenses_cursor)

    return JsonResponse({'expenses': expenses})

@login_required
def get_incomes(request):
    user = request.user
    filter_type = request.GET.get('filter', 'this_month')

    # Access MongoDB collection directly
    with connection.cursor() as cursor:
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

        incomes_cursor = income_collection.find({
            'user_id': user.id,
            'date': {'$gte': start_date}
        })
        incomes = sum(Decimal(income['amount'].to_decimal()) for income in incomes_cursor)

    return JsonResponse({'incomes': incomes})

@login_required
def get_weekly_balance(request):
    user = request.user
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = today - timedelta(days=6)

    with connection.cursor() as cursor:
        db = cursor.db_conn
        income_collection = db['incomes_income']
        expense_collection = db['expenses_expense']

        balances = []
        for i in range(7):
            day = start_date + timedelta(days=i)
            next_day = day + timedelta(days=1)

            incomes_cursor = income_collection.find({
                'user_id': user.id,
                'date': {'$gte': day, '$lt': next_day}
            })
            expenses_cursor = expense_collection.find({
                'user_id': user.id,
                'date': {'$gte': day, '$lt': next_day}
            })

            total_incomes = sum(Decimal(income['amount'].to_decimal()) for income in incomes_cursor)
            total_expenses = sum(Decimal(expense['amount'].to_decimal()) for expense in expenses_cursor)
            balance = total_incomes - total_expenses

            balances.append({
                'date': day.strftime('%Y-%m-%d'),
                'balance': float(balance)
            })

    return JsonResponse({'balances': balances})