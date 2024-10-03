import asyncio
import pandas as pd
from binance.client import AsyncClient
import aiohttp
import concurrent.futures
from dateutil.relativedelta import relativedelta


import datetime

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
        
        print(f'Fetched {len(df)} rows of data')
        return df

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        if client:
            await client.close_connection()
        if 'session' in locals():
            await session.close()

async def fetch_all_months_new(symbol, interval, start, end):
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


def fetch_data_sync(symbol, interval, start, end):
    try:
        # Check if we're in the main thread or another thread
        try:
            # Try to get the current loop (this works in the main thread)
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # If there's no running loop, we need to create one for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # If the loop is already running (e.g., in FastAPI or Django's async environment)
        if loop.is_running():
            # Use a ThreadPoolExecutor to run the coroutine in a thread
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(lambda: asyncio.run(fetch_all_months_new(symbol, interval, start, end)))
                return future.result()
        else:
            # If the loop is not running, run the coroutine directly
            return asyncio.run(fetch_all_months_new(symbol, interval, start, end))
    except Exception as e:
        print(f"Error in fetch_data_sync: {e}")
        return None

