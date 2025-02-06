from django.shortcuts import render, redirect
from django.conf.urls import handler404

def homepage (request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('student_list')
        else:
            return redirect('my_schedules')
    else:
        return redirect('login')

