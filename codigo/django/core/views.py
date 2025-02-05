from django.shortcuts import render, redirect
from django.conf.urls import handler404

def homepage (request):
    return redirect('student_list')

