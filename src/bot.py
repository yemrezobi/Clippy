from discord.ext import commands
from discord import FFmpegPCMAudio
from os import path
import asyncio

last = None
# get token from token.txt
with open("../token.txt", "r") as f:
    TOKEN = f.read()

bot = commands.Bot(command_prefix=["clip!", "c!"])


@bot.event
async def on_ready():
    print("I'm ready to go!")


@bot.command(aliases=["p"])
async def play(ctx, *args):

    if len(args) == 0 or ctx.author.voice is None:
        if len(args) == 0:
            print("No args, idiot.")
        if ctx.author.voice is None:
            print("Connect to voice, idiot.")
        return
    file = "../clips/" + args[0] + ".mp3"
    if not path.exists(file):
        print("No such file (" + args[0] + ".mp3)")
        await ctx.reply(args[0] + " does not exist.")
        return
    global last
    last = args[0]
    user_channel = ctx.author.voice.channel

    # mama's spaghetti inc
    voice_client = None
    if ctx.me.voice is None or ctx.me.voice.channel != user_channel:
        voice_client = await user_channel.connect()

    voice_client.play(FFmpegPCMAudio(file))
    while voice_client.is_playing():
        await(asyncio.sleep(0.2))

    try:
        if ctx.me.voice.channel is not None:
            await voice_client.disconnect()
    except AttributeError:
        # this happens due to a race condition when multiple events try to disconnect
        pass


@bot.command(aliases=["r"])
async def random(ctx):
    await ctx.send("so random lol xd")


@bot.command(aliases=["re"])
async def replay(ctx):
    if last is None:
        return
    await play(ctx, last)


bot.run(TOKEN)
