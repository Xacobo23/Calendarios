from django.shortcuts import render, redirect

from .models import Class
#from .forms import ClassForm

def class_list (request):
    classes = Class.objects.all()
    return render(request, 'class_list.html', {'classes': classes})
