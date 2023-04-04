import asyncio
import aiohttp
import json
import random
import discord
import os

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

def truncate_text(text: str, limit: int, ellipsis: str = "...") -> list[str]:
    if len(text) > limit:
        texts = [text[: limit - len(ellipsis)] + ellipsis]
        pos = limit - len(ellipsis)
        while pos < len(text):
            if pos + limit - len(ellipsis) < len(text):    
                span = limit - len(ellipsis) * 2
                texts.append(ellipsis + text[pos:pos + span] + ellipsis)
                pos+= span
            else:
                texts.append(ellipsis + text[pos:len(text)])
                return texts
        return texts
    else:
        return [text]

def random_color():
    return discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)