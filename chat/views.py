from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

from django.http import HttpResponse

@login_required
def index(request):
    return render(request, 'index.html')

def register(request):
    
    if request.method == "GET":
        return render(request, 'register.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = request.POST.get('type')

        User.objects.create_user(username=username, password=password, is_staff=admin)

        return redirect('/chat/')