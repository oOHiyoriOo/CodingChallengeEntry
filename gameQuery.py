import discord
import asyncio
from ZeroLogger.ZeroLogger import *
import config
import random
from tinydb import TinyDB, Query

botVersion = 0.2

query = Query()
Players = TinyDB('player.json')

intents = discord.Intents(messages=True,guilds=True)

client = discord.Client(intents=intents)

Running = False
Searching = False

@client.event
async def on_ready():
    logo(["==============================","Bot is Ready","=============================="])
    # Setting `Playing ` status
    await client.change_presence(activity=discord.Game(name="Running on version: "+str(botVersion)))
    await asyncio.sleep(5)
    await client.change_presence(activity=discord.Game(name="THE Game. "+random.choice([":3",":)",";3","<3"] ) ) )

@client.event
async def on_message(msg):
    await client.wait_until_ready()
    if msg.channel.id == 772484220253503509:

        global Searching

        
        if msg.content == "*start" and not Running and not Searching:
            Players.append(msg.author.id)
            omsg = await msg.channel.send("Starting a game, everyone has 60 sec. to join!")
            Searching = True
            await msg.delete()
            await GameLobby(omsg)


        elif msg.content == "*join" and not Running and Searching:
            if not msg.author.id in Players:
                Players.insert({"user":msg.author.id})
            await msg.delete()



async def GameLobby(omsg):
    await client.wait_until_ready()
    global Searching
    global Running

    for i in range(60):
        await omsg.edit(content="Starting a game, everyone has "+str(60 -i)+" sec. to join!")
        await asyncio.sleep(1)

    await omsg.edit(content="Game Starts!")
    Searching = False
    Running = True
    
    for Player in Players.search(query.user >= 0):
        print(Player)


client.run(config.token)