from django.shortcuts import render, redirect

from .models import Classroom

def class_list (request):
    classes = Classroom.objects.all()

    data = {
        'classes': classes
    }

    return render(request, 'class_list.html', classes)
