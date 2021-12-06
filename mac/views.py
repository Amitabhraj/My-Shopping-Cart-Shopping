from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse


def check_login(request):
	if request.user.is_authenticated:
		return redirect('/shop')
	return render(request, 'accounts/login.html')