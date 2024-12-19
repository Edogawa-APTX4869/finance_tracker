from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Income, Source
from userpreferences.models import userPreferences
from django.http import JsonResponse
from django.core.paginator import Paginator
from decimal import Decimal
from django.db import connection
from datetime import datetime, timedelta

@login_required()
def index(request):
    incomes = Income.objects.filter(user=request.user).order_by('-id')
    for income in incomes:
        income.category_name = income.source.name

    paginator = Paginator(incomes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    currency = userPreferences.objects.get(user=request.user).currency
    context = {
        'incomes': incomes,
        'page_obj': page_obj,
        'currency': currency
    }

    return render(request, 'App/Incomes/index.html', context)

@login_required
def add_income(request):
    if request.method == 'POST':
        source_id = request.POST.get('incomeSource')
        amount = request.POST.get('incomeAmount')
        date = request.POST.get('incomeDate')
        description = request.POST.get('description', '')

        source = Source.objects.get(id=source_id)
        Income.objects.create(
            user=request.user,
            source=source,
            amount=amount,
            description=description,
            date=date
        )
        messages.success(request, 'Income added successfully.')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': '/incomes/'})

        return redirect('incomes')

    currency = userPreferences.objects.get(user=request.user).currency
    sources = list(Source.objects.values('id', 'name'))

    context = {
        'sources': sources,
        'currency': currency
    }

    return render(request, 'App/incomes/add-income.html', context)

@login_required
def edit_income(request, income_id):
    income = Income.objects.get(id=income_id)
    if request.method == 'POST':
        source_id = request.POST.get('incomeSource')
        amount = request.POST.get('incomeAmount')
        date = request.POST.get('incomeDate')
        description = request.POST.get('description', '')

        source = Source.objects.get(id=source_id)
        income.source = source
        income.amount = amount
        income.date = date
        income.description = description
        income.save()
        messages.success(request, 'Income updated successfully.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect': '/incomes/'})
        return redirect('incomes')

    sources = list(Source.objects.values('id', 'name'))
    currency = userPreferences.objects.get(user=request.user).currency
    context = {
        'income': income,
        'sources': sources,
        'currency': currency
    }
    return render(request, 'App/incomes/edit-income.html', context)

@login_required
def delete_income(request, income_id):
    income = Income.objects.get(id=income_id)
    income.delete()
    messages.success(request, 'Income deleted successfully.')
    return redirect('incomes')

@login_required
def income_sources_summary(request):
    user = request.user
    filter_type = request.GET.get('filter', 'this_month')

    finalrep = {}
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

        # Calculate totals by source
        source_totals = {}
        for income in incomes_cursor:
            source = income['source_id']
            amount = Decimal(income['amount'].to_decimal())
            if source in source_totals:
                source_totals[source] += amount
            else:
                source_totals[source] = amount

    sources = {str(source.id): source.name for source in Source.objects.all()}
    x_values = [sources.get(str(source_id), "Unknown") for source_id in source_totals.keys()]
    y_values = [float(total) for total in source_totals.values()]

    return JsonResponse({'xValues': x_values, 'yValues': y_values})