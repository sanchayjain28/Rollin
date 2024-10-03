from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .helper import fetch_data_sync


def fetch_binance_data(request):
    return render(request, 'fetch_data/fetch_ticker.html', {
    })

def fetch_binance_data(request):
    data_to_return = []
    error_message = None

    if 'symbol' in request.GET:
        symbol = request.GET.get('symbol')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        candle = request.GET.get('candle', '1d')

    else:
        return render(request, 'fetch_data/fetch_ticker.html', {
            'data': data_to_return,
            'error': "Symbol is required"
        })
    a = 0

    try:
        historical_data = fetch_data_sync(symbol, candle, start_date, end_date)
        data_to_return = [
            [row['datetime'],
             row['open'], 
             row['high'],
             row['low'],
             row['close'],
             row['volume']
             ]
            for index, row in historical_data.iterrows()
        ]
    except Exception as e:
        error_message = str(e)
        print(error_message)
    return render(request, 'fetch_data/fetch_ticker.html', {
        'data': data_to_return,
        'error': error_message
    })
