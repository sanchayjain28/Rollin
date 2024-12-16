from django.urls import path

from .views import *
urlpatterns = [
    path("", show_blogs, name="blogs"),
    path("<int:blg_id>/", show_blog, name="blog"),
    path("create", create_blog, name="create_blog"),

    ]
