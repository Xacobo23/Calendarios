from django.shortcuts import render, redirect

from .forms import RegisterForm

# Create your views here.

def login (request):
    return render(request, 'login.html', {'title': 'Login'})

def register (request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = RegisterForm()

    return render (request, 'registration/register.html', {'form': form})