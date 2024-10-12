import asyncio
import datetime
import aiohttp
import pandas as pd
import concurrent.futures
from binance.client import AsyncClient
from binance.exceptions import BinanceAPIException
from dateutil.relativedelta import relativedelta

from config.logger import logger


async def fetch_monthly_data_async(symbol, interval, start, end):
    client = None
    try:
        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
      
        client = AsyncClient()
        

        data_raw = await client.futures_historical_klines(symbol, interval, start, end)

        if not data_raw or not isinstance(data_raw, list):
            print("No data or data is not in list format")
            return None

        df = pd.DataFrame(data_raw, columns=[
            "datetime", "open", "high", "low", "close", "volume", 
            "close_time", "quote_asset_volume", "number_of_trades", 
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])

        df = df.iloc[:, :6]
        df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].apply(pd.to_numeric, errors="coerce")
        
        logger.info(f'Fetched {len(df)} rows of data')
        return df

    except BinanceAPIException as e:
        logger.error("Error processing")
        raise 
        
    finally:
        if client:
            await client.close_connection()
        if 'session' in locals():
            await session.close()

async def fetch_all_months_new(symbol, interval, start, end):
    try:
        if start and end:
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
        else:
            end_date = datetime.datetime.now() - datetime.timedelta(days=1)
            start_date = end_date - datetime.timedelta(days=4 * 365)

        current_date = datetime.datetime.now()
        if end_date > current_date:
            end_date = current_date

        months = []
        current = start_date
        while current <= end_date:
            months.append(current)
            current += relativedelta(months=1)

        if months and months[-1] <= end_date:
            months.append(end_date)

        tasks = []
        for i in range(len(months) - 1):
            month_start = months[i].strftime("%Y-%m-%d")
            month_end = (months[i + 1] if i + 1 < len(months) else end_date).strftime("%Y-%m-%d")
            tasks.append(fetch_monthly_data_async(symbol, interval, month_start, month_end))

        results = await asyncio.gather(*tasks)

        dataframes = [result for result in results if result is not None]

        if dataframes:
            data = pd.concat(dataframes)
            data = data.drop_duplicates(subset="datetime")
            data = data.reset_index(drop=True)
            return data
        else:
            return pd.DataFrame()
    except:
        raise



def fetch_data_sync(symbol, interval, start, end):
    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(lambda: asyncio.run(fetch_all_months_new(symbol, interval, start, end)))
                return future.result()
        else:
            return asyncio.run(fetch_all_months_new(symbol, interval, start, end))
    except Exception as e:
        print(f"Error in fetch_data_sync: {e}")
        raise 

