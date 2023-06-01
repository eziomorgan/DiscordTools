import openai
import copy
import uuid
import os
from Utilities import exception_handler_decorator, download_file, create_folder, config

openai.api_key = config["openai_key"]
original_message = [
    {"role": "system", "content": "You are a helpful assistant."},
]
save_image = config["save_images"].lower()
save_audio = config["save_audio"].lower()
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
        model = 'gpt-4',
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
    if save_image == "true":
        create_folder(".\\img\\")
        img_name = f".\\img\\{uuid.uuid4()}.png"
        await download_file(response['data'][0]['url'], img_name)
    return response['data'][0]['url']

@exception_handler_decorator
async def speech_to_text(url, mode):
    local_filename = f".\\audio\\{uuid.uuid4()}.mp3"
    await download_file(url, local_filename)
    with open(local_filename, "rb") as audio_file:
        if mode == 0:
            transcripts = openai.Audio.transcribe("whisper-1", audio_file)
        else:
            transcripts = openai.Audio.translate("whisper-1", audio_file)
    if save_audio == "false" and os.path.exists(local_filename):
        os.remove(local_filename)
    return transcripts

@exception_handler_decorator
async def clear_history(channel_id):
    global message_channels 
    if channel_id in message_channels:
        del message_channels[channel_id]


