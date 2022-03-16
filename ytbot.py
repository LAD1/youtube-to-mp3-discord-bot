from discord_components import *
from discord.ext import commands
from pytube import YouTube
import discord
import asyncio
import os


token = "token"
client = commands.Bot(command_prefix="#", help_command=None, case_sensitive=False)

@client.command(pass_context=True,aliases=['download','d'])
async def dl(ctx, arg):
    if arg == None:
        await ctx.send('Please provide a URL')
    else:
        try:
            yt = YouTube(arg)
            await ctx.message.delete()
            await ctx.send("Downloading audio...", delete_after=2)
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download()
            base, ext = os.path.splitext(out_file)
            new_file = base + ".mp3"
            os.rename(out_file, new_file)
            await ctx.send("Uploading audio...", delete_after=2)
            await ctx.send(yt.title,file=discord.File(new_file))
            os.remove(new_file)
        except Exception as e:
            await ctx.send("Error: "+str(e))
            os.remove(new_file)

@client.event
async def on_ready():
    DiscordComponents(client)
    print('Running - bot')
    print('--------------------------------------')
client.run(token)