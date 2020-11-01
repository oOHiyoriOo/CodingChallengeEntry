import discord
import asyncio
from ZeroLogger.ZeroLogger import *
import config


botVersion = 0.1

intents = discord.Intents(messages=True)

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logo(["==============================","Bot is Ready","=============================="])
    # Setting `Playing ` status
    await client.change_presence(activity=discord.Game(name="Running on version: "+str(botVersion)))




@client.event
async def on_message(msg):
    warn(msg.content)

client.run(config.token)