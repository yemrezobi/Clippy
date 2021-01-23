import discord
from discord.ext import commands

TOKEN = ""

client = commands.Bot(command_prefix="clip!")


@client.event
async def on_ready():
    print("I'm ready to go!")


client.run(TOKEN)