from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import login_view, logout_view
urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", obtain_auth_token, name="signup"),
    path("logout/", logout_view, name="logout"),
    ]
