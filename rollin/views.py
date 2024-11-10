from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

def home(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'signup.html', {'form': form})