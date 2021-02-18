from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import Embed
from os import path
from os import listdir
from random import choice
import asyncio

MAX_QUEUE_LENGTH = 5
last = None
queue = []
playing = False
# get token from token.txt
with open("../token.txt", "r") as f:
    TOKEN = f.read()

bot = commands.Bot(command_prefix=["clip!", "c!"], help_command=None)


@bot.event
async def on_ready():
    print("I'm ready to go!")


@bot.command(aliases=["h"])
async def help(ctx):
    desc = ("help: guess what this does\n"
            "play <clip>: plays the given clip (eg. clip!play test)\n"
            "random: plays a random clip\n"
            "replay: replays the last clip played\n"
            "list: lists all clips\n")
    embed = Embed(title="**Commands**", color=0x0660bd)
    embed.description = desc
    await ctx.send(embed=embed)


@bot.command(aliases=["p"])
async def play(ctx, *args):

    if len(args) == 0:
        print("No arguments found.")
        return

    file = "../clips/" + args[0] + ".mp3"
    if not path.exists(file):
        print("No such file (" + args[0] + ".mp3)")
        await ctx.reply(args[0] + " does not exist.")
        return

    voice_client = await connect(ctx)
    if voice_client is False:
        print("Could not connect.")
        return
    elif voice_client is None:
        voice_client = ctx.author.voice.channel

    if len(queue) <= MAX_QUEUE_LENGTH:
        queue.append(file)

    if playing is False:
        await play_queue(ctx, voice_client)


@bot.command(aliases=["r"])
async def random(ctx):
    r = choice(listdir("../clips"))
    r = r[:-4]
    await play(ctx, r)


@bot.command(aliases=["re"])
async def replay(ctx):
    if last is None:
        return
    await play(ctx, last)


@bot.command(aliases=["l"])
async def list(ctx):
    files = listdir("../clips")
    for i in range(len(files)):             # remove file extensions (removes 4 characters, might be an issue with
        files[i] = files[i][:-4]            # extensions with more or less characters)
    message = ", ".join(files)
    embed = Embed(title="**Clips**", color=0xd71e3e)
    embed.description = message
    await ctx.send(embed=embed)


async def connect(ctx):
    if ctx.author.voice is None:
        print("User not connected to voice.")
        return

    user_channel = ctx.author.voice.channel

    if ctx.me.voice is None or ctx.me.voice.channel != user_channel:
        voice_client = await user_channel.connect()
        return voice_client
    elif ctx.me.voice.channel is user_channel:
        return None
    else:
        print("Something went wrong!")
        return False


async def disconnect(ctx, voice_client):
    try:
        if ctx.me.voice.channel is not None:
            await voice_client.disconnect()
    except AttributeError:
        # this happens due to a race condition when multiple events try to disconnect
        raise


async def play_queue(ctx, voice_client):
    global playing
    playing = True

    global last

    while len(queue) > 0:
        last = queue.pop(0)

        voice_client.play(FFmpegPCMAudio(last))
        while voice_client.is_playing():
            await asyncio.sleep(0.2)

    playing = False

    await disconnect(ctx, voice_client)


bot.run(TOKEN)
