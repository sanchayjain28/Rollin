from django.shortcuts import render
from rest_framework.authtoken.views import obtain_auth_token
from config.logger import logger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
# Create your views here.

def login_view(request):
    if request.method == "POST":
        obtain_auth_token(request)
    else:
        return render(request, "login.html")

@api_view(['POST'])
def logout_view(request):
    """
    Logout a user by deleting their authentication token.
    """
    if request.user.is_authenticated:
        try:
            # Delete the user's token
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
