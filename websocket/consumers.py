import json
import asyncio
import websockets
from config.logger import logger
from channels.generic.websocket import AsyncWebsocketConsumer


class BTCTicker(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  
        logger.info("WebSocket connection accepted.")
        self.subscriptions = {}  

    async def disconnect(self, close_code):
        # Unsubscribe from all symbols when disconnecting
        for symbol in list(self.subscriptions.keys()):
            await self.unsubscribe(symbol)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_symbol = text_data_json.get('symbol', 'btcusdt').lower()
        symbols = ['btcusdt', 'ethdusdt', 'xrpusdt', 'ltcusdt', 'bnbusdt', 'adausdt', 'dogeusdt']  
        for user_symbol in symbols:
            if user_symbol not in self.subscriptions:  # Only subscribe if not already subscribed
                await self.subscribe(user_symbol)

        await self.send(text_data=json.dumps({
            'message': f'Subscribed to {user_symbol}',
            'status': 'Subscribed to Binance WebSocket'
        }))

    async def subscribe(self, symbol):
        """Subscribe to a new symbol."""
        if symbol in self.subscriptions:
            logger.info(f"Already subscribed to {symbol}")
            return  # Prevent re-subscribing

        logger.info(f"Subscribing to {symbol}")
        self.subscriptions[symbol] = asyncio.create_task(self.fetch_symbol_avg_price(symbol))

    async def unsubscribe(self, symbol):
        """Unsubscribe from a symbol."""
        if symbol in self.subscriptions:
            task = self.subscriptions[symbol]
            task.cancel()  # Cancel the task
            del self.subscriptions[symbol]  # Remove it from subscriptions
            logger.info(f"Unsubscribed from {symbol}")

    async def fetch_symbol_avg_price(self, symbol):
        binance_ws_url = 'wss://testnet.binance.vision/ws'
        try:
            async with websockets.connect(binance_ws_url) as websocket:
                subscribe_message = {
                    "method": "SUBSCRIBE",
                    "params": [f"{symbol}@avgPrice"],
                    "id": 1
                }
                logger.info(f"Sending subscribe message for {symbol}: {subscribe_message}")
                await websocket.send(json.dumps(subscribe_message))

                while True:
                    binance_data = await websocket.recv()
                    binance_data_json = json.loads(binance_data)
                    logger.info(f"Received data for {symbol}: {binance_data_json}")

                    avg_price = binance_data_json.get('w')  # Average price key
                    await self.send(text_data=json.dumps({
                        'symbol': symbol,
                        'price': avg_price
                    }))
                    
                    await asyncio.sleep(1)  # Adjust frequency as needed

        except asyncio.CancelledError:
            logger.info(f"Task for {symbol} was cancelled.")
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
