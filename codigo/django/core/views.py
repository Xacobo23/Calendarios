from django.shortcuts import render, redirect

def homepage (request):
    return redirect('student_list')
