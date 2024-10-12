from channels.generic.websocket import AsyncWebsocketConsumer
import json
import websockets
import asyncio

from config.logger import logger

class BTCTicker(AsyncWebsocketConsumer):
    async def connect(self):
        self.symbol = "btcusdt"
        await self.accept()
        self.binance_task = asyncio.create_task(self.fetch_bnb_avg_price())



    async def disconnect(self, close_code):
        if not self.binance_task.cancelled():
            self.binance_task.cancel()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.symbol = text_data_json.get('symbol', 'btcusdt').lower()

        await self.send(text_data=json.dumps({
            'message': f'You said: hii',
            'status': 'Connected to Binance WebSocket' 
        }))

    async def fetch_bnb_avg_price(self):
        binance_ws_url = 'wss://testnet.binance.vision/ws'
        try:
            async with websockets.connect(binance_ws_url) as websocket:
                subscribe_message = {
                    "method": "SUBSCRIBE",
                    "params": [f"{self.symbol}@avgPrice"],
                    "id": 1
                }
                print(subscribe_message)
                await websocket.send(json.dumps(subscribe_message))
                while True:
                    binance_data = await websocket.recv()
                    binance_data_json = json.loads(binance_data)
                    logger.info(binance_data_json)
                    avg_price = binance_data_json.get('w')

                    await self.send(text_data=json.dumps({
                        'price': avg_price
                    }))
                    await asyncio.sleep(1)

        except Exception as e:
            print(f"Error fetching data from Binance: {e}")
