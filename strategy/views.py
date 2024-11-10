# views.py
from django.shortcuts import render
from django.http import HttpResponse
from config.logger import logger

def home(request):
    if request.method == 'POST':
        logger.info("POST: %s" % request)
        indicator = request.POST.get('indicator')

        default_values = {
            'rsi': {'time': 14},
            'adx': {'time': 14, 'smoothing': 3},
            'macd': {'fast': 12, 'slow': 26, 'signal': 9},
        }
        # Gather parameters based on selected indicator
        if indicator == 'rsi':
            rsi_time = request.POST.get('rsi_time') or default_values['rsi']['time']
            response = f"Selected RSI with Time Period: {rsi_time}"
        
        elif indicator == 'adx':
            adx_time = request.POST.get('adx_time') or default_values['adx']['time']
            adx_smoothing = request.POST.get('adx_smoothing') or default_values['adx']['smoothing']
            response = f"Selected ADX with Time Period: {adx_time} and Smoothing: {adx_smoothing}"
        
        elif indicator == 'macd':
            macd_fast = request.POST.get('macd_fast') or default_values['macd']['fast']
            macd_slow = request.POST.get('macd_slow') or default_values['macd']['slow']
            macd_signal = request.POST.get('macd_signal') or default_values['macd']['signal']
            response = f"Selected MACD with Fast Period: {macd_fast}, Slow Period: {macd_slow}, Signal Period: {macd_signal}"
        
        else:
            response = "No valid indicator selected."
            return HttpResponse(response)
        return HttpResponse(response)
    elif request.method == "GET": 
        render(request, template_name='indicators/home.html')
    return render(request, 'indicators/home.html')
