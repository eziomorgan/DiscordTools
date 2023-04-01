import openai
import copy
from Utilities import exception_handler_decorator, download_file, config

openai.api_key = config["openai_key"]
original_message = [
    {"role": "system", "content": "You are a helpful assistant."},
]
messages = copy.deepcopy(original_message)
message_channels = {}

@exception_handler_decorator
async def generate_response(prompt, channel_id):
    global message_channels 
    if channel_id in message_channels:
        messages = message_channels[channel_id]  
    else: 
        messages = copy.deepcopy(original_message)
        message_channels[channel_id] = messages

    prompt_msg = {"role": "user", "content": prompt}
    messages.append(prompt_msg)
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages= messages
    )
    reply = response['choices'][0]['message']['content']
    reply_msg = {"role": "assistant", "content": reply}
    messages.append(reply_msg)
    return reply

@exception_handler_decorator              
async def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

@exception_handler_decorator
async def transcribe(url):
    local_filename = "temp_audio.mp3"
    await download_file(url, local_filename)
    audio_file = open(local_filename, "rb")
    return openai.Audio.transcribe("whisper-1", audio_file)

@exception_handler_decorator
async def clear_history(channel_id):
    global message_channels 
    if channel_id in message_channels:
        del message_channels[channel_id]


