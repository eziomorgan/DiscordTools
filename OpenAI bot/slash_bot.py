import discord
import openai_helper 
from Utilities import exception_handler_decorator, config

discord_token = config["discord_token"]
bot = discord.Bot()
agi = bot.create_group("agi", "openai api commands")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@exception_handler_decorator
@agi.command(description="responde to question")
async def chat_complete(ctx, msg: str):
    if ctx.author == bot.user:
        return

    await ctx.defer()
    response = await openai_helper.generate_response(msg, ctx.channel_id)
    await ctx.followup.send(f"❓: {msg}\n ✅:{response}")

@exception_handler_decorator
@agi.command(description="reset bot chat history")
async def memento(ctx):
        await ctx.defer()
        await openai_helper.clear_history(ctx.channel_id)
        await ctx.followup.send(f"bot chat history reset ✅")

@exception_handler_decorator
@agi.command(description="generate an image from text")
async def imagine(ctx, prompt:str):
    await ctx.defer()
    image_url = await openai_helper.generate_image(prompt)
    embed = discord.Embed()
    if image_url:
        embed.set_image(url=image_url)
        await ctx.followup.send(f"🎨 {prompt}\n", embed=embed)
    else:
        await ctx.followup.send(f"🎨 {prompt}\n 🚫 content not allowed", )

@exception_handler_decorator
@agi.command(description="transcribe audio file")
async def transcribe(ctx, message_link:str):
    await speech_to_text(ctx, message_link, 0)

@exception_handler_decorator
@agi.command(description="translate audio file")
async def translate(ctx, message_link:str):
    await speech_to_text(ctx, message_link, 1)

@exception_handler_decorator
async def speech_to_text(ctx, message_link:str, mode):
    try:
        await ctx.defer()
        splits = message_link.split('/')
        _, _, _, _, guild_id, channel_id, message_id = message_link.split('/')
        if guild_id == "@me":
            channel = await bot.fetch_channel(int(channel_id))
        else:
            guild = bot.get_guild(int(guild_id))
            channel = guild.get_channel(int(channel_id))

        message = await channel.fetch_message(int(message_id))
        if message.attachments:
            audio_attachment = message.attachments[0]
        #MIME type
        if audio_attachment.content_type == 'audio/mpeg':         
            transcript = await openai_helper.speech_to_text(audio_attachment.url, mode)
            await ctx.followup.send(f"🎵 {message_link}\n📝 {transcript.text}")
        else:
            await ctx.followup.send(f"🚫 require mp3 file")
    except Exception as e:
        await ctx.followup.send(f"🚫 Caught an exception: {e}")


@exception_handler_decorator
@bot.command(description="delete channel msgs, <= 0 to purge")
async def clear(ctx, amount:int):
    await ctx.defer()
    purge = True if amount <= 0 else False
    amount = amount + 1 if amount > 0 else amount
    while True:
        if amount > 0 and amount < 100:
            limit = amount
        else:
            limit = 100
        fetched_messages = await ctx.channel.history(limit=limit).flatten()
        #avoid deleting the current ongoing message
        fetched_messages.pop(0) 
        if len(fetched_messages) == 0:
            break
        delete_cnt = 0
        for message in fetched_messages:
            try:
                await message.delete()
                delete_cnt += 1
            except Exception as e:
                print(f"💥Caught an exception : {e}")
        if delete_cnt == 0:
            break
        if not purge:
            amount -= len(fetched_messages)
            if amount <= 0:
                break

    await ctx.followup.send(f"channel chat msgs deleted ✅")


bot.run(discord_token)