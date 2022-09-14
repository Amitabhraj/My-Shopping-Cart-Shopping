from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import *

def check_login(request):
    if request.user.is_authenticated:
        return redirect('/shop')
    else:
        return redirect('/shop/login')
    return render(request, 'accounts/login.html')




