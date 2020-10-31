import discord
from ZeroLogger.ZeroLogger import *
import config

client = discord.Client()


@client.event
async def on_ready():
    logo(["==============================","Bot is Ready","=============================="])

@client.event
async def on_message(msg):
    warn(msg.content)



client.run(config.token)
