from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .forms import UserCreateForm

def admin_panel (request):
    return render(request, 'admin.html')

class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list') 

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)
