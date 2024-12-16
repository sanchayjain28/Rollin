from django.http import HttpResponse
from .models import Blogs
# Create your views here.

def show_blogs(request):
    data = Blogs.objects.all()
    data = list(data.values())
    return HttpResponse(data)

def show_blog(request, blg_id):
    return HttpResponse("This is a blog")

def create_blog(request):
    return HttpResponse("Create a new blog")