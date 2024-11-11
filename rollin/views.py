from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from config.logger import logger
def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  
            django_login(request, user)  
            logger.info(f"User {user.username} logged in successfully.")
            return redirect('home') 
        else:
            logger.error(f"Login failed for user {request.POST.get('username')}")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout(request):
    logger.info(f"User {request.user.username} attempting to log out.")  
    if request.user.is_authenticated:
        logger.info(f"User {request.user.username} logged out successfully.")
        django_logout(request)
    return redirect('home')

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
            login(request)
            logger.info(f"User {user.username} created and logged in.")
            return redirect('home')
        else:
            form_data = form.cleaned_data
            logger.error(f"Form errors: {form.errors} {form_data}")
            return render(request, 'signup.html', {'form': form, "errors": form.errors})
