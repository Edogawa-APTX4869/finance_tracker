from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import userPreferences

# Create your views here.
@login_required()
def settings(request):
    exists = userPreferences.objects.filter(user=request.user).exists()
    if exists:
        user_Preferences = userPreferences.objects.get(user=request.user)
    else:
        user_Preferences = userPreferences(user=request.user)
        user_Preferences.save()

    currency_data = []
    with open('static/assets/currencies.json') as f:
        data = json.load(f)
        for key, value in data.items():
            currency_data.append({'name': key, 'value': value})

    if request.method == 'POST':
        currency = request.POST.get('currency')
        user_Preferences.currency = currency
        user_Preferences.save()
        messages.success(request, 'Currency Changed Successfully')

    return render(request, 'App/Userpreferences/index.html', {
        'currencies': currency_data,
        'user_currency': user_Preferences.currency
    })