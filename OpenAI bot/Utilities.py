import asyncio
import aiohttp
import json

def load_config(file_path):
    with open(file_path, "r") as file:
        config = json.load(file)

    return config

config = load_config("config.json")

def exception_handler_decorator(func):
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Caught an exception in {func.__name__}: {e}")
            return None

    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f"Caught an exception in {func.__name__}: {e}")
            return None

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

async def download_file(url, local_filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(local_filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)



