from django.shortcuts import render

# Create your views here.

def socket(request):
    return render(request, 'websocket/websocket.html')