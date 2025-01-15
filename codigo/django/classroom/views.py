from django.shortcuts import render, redirect

from .models import Classroom
#from .forms import ClassForm

def class_list (request):
    classes = Classroom.objects.all()
    return render(request, 'class_list.html', {'classes': classes})
