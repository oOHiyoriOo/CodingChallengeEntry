import discord
import asyncio
from ZeroLogger.ZeroLogger import *
import config


botVersion = 0.2

intents = discord.Intents(messages=True)

client = discord.Client(intents=intents)

Players = []
Running = False
Searching = False

@client.event
async def on_ready():
    logo(["==============================","Bot is Ready","=============================="])
    # Setting `Playing ` status
    await client.change_presence(activity=discord.Game(name="Running on version: "+str(botVersion)))
    asyncio.sleep(5)
    await client.change_presence(activity=discord.Game(name="THE Game."))

@client.event
async def on_message(msg):
    if msg.channel.id == 772484220253503509:
        global Players
        global Searching

        
        if msg.content == "*start" and Running == False and Searching == False:
            Players.append(msg.author.id)
            omsg = await msg.channel.send("Starting a game, everyone has 60 sec. to join!")
            Searching = True
            client.loop.create_task(GameLobby(omsg)) 

        elif msg.content == "*join" and Running == False and Searching == True:
            Players.append(msg.author.id)



async def GameLobby(omsg):
    if client.is_ready():
        global Players
        global Searching
        
        for i in range(60):
            await omsg.edit("Starting a game, everyone has "+str(60 -i)+" sec. to join!")

    else:
        raise Exception("Client is not ready!")


client.run(config.token)