from django.shortcuts import render
from rest_framework.authtoken.views import obtain_auth_token
from config.logger import logger
# Create your views here.

def login_view(request):
    if request.method == "POST":
        print("ii")
        obtain_auth_token(request)
    else:
        return render(request, "login.html")
