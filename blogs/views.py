from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogs
# Create your views here.

def show_blogs(request):
    data = Blogs.objects.all()
    data = list(data.values())
    return HttpResponse(data)