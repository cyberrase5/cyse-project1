from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import Messages
from datetime import date
import sqlite3

# Create your views here.

@login_required
def index(request):
    if request.method == 'GET':
        admin = User.objects.get(username=request.user).is_staff
        messages = Messages.objects.all()
        return render(request, 'index.html', {'admin': admin, 'messages': messages})
    if request.method == 'POST':
        content = request.POST.get('content')
        Messages.objects.create(sender=request.user, content=content)

        return redirect('/chat/')

def register(request):
    
    if request.method == "GET":
        return render(request, 'register.html', {'msg': ""})
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = request.POST.get('type')

        # app crashes if name is not unique, test it here
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        sql = "SELECT username FROM auth_user WHERE username='" + username + "'"
        response = cursor.execute(sql).fetchall()
        
        # response returns a list
        if len(response) != 0:
            return render(request, 'register.html', {'msg': f'Username {response} already in use'})

        # Insufficient Logging & Monitoring
        # log_register(request, username)

        User.objects.create_user(username=username, password=password, is_staff=admin)

        return redirect('/chat/')

# BROKEN ACCESS CONTROL
# @staff_member_required
def admin(request):
    messages = Messages.objects.all()
    return render(request, 'admin.html', {'messages': messages})

@staff_member_required
def delete(request, message_id):
    message = Messages.objects.get(id=message_id)
    
    message.delete()
    return redirect('/chat/admin')

@staff_member_required
def logs(request):
    f = open("log.txt", "r")
    logs = []

    for row in f:
        logs.append(row)

    return render(request, 'logs.html', {'logs': logs})

# auxiliary functions

def log_register(request, username):
        ip_addr = request.META['REMOTE_ADDR']
        f = open("log.txt", "a")
        f.write(f"{date.today()} --- {ip_addr} registered account {username} \n")
        f.close()