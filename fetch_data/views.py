from django.shortcuts import render
from binance.exceptions import BinanceAPIException

from .helper import fetch_data_sync
from config.logger import logger

def fetch_binance_data(request):
    data_to_return = []
    error_message = None

    # Check if the request contains query parameters for 'symbol'
    if 'symbol' in request.GET:
        symbol = request.GET.get('symbol')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        candle = request.GET.get('candle', '1d')  # Default to '1d' if not provided

        if not symbol:
            error_message = "Symbol is required"
        else:
            try:
                # Fetch historical data
                historical_data = fetch_data_sync(symbol, candle, start_date, end_date)
                data_to_return = [
                    [
                        row['datetime'],
                        row['open'], 
                        row['high'],
                        row['low'],
                        row['close'],
                        row['volume']
                    ]
                    for index, row in historical_data.iterrows()
                ]
            except BinanceAPIException as e:
                logger.error(str(e))
                error_message = e.message

    # Render the template without error if no query parameters are provided
    return render(request, 'fetch_data/fetch_ticker.html', {
        'data': data_to_return,
        'error': error_message
    })
