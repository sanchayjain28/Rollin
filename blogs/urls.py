from django.urls import path

from .views import show_blogs
urlpatterns = [
    path("", show_blogs, name="blogs"),
    ]
