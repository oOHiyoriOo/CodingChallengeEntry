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
AllBets = 0
 

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
            Players.insert({"user":msg.author.id,"votes":1000,"currentBet":0})
            omsg = await msg.channel.send("Starting a game, everyone has 60 sec. to join!")
            Searching = True
            await msg.delete()
            await GameLobby(omsg)


        elif msg.content == "*join" and not Running and Searching:
            if not msg.author.id in Players:
                Players.insert({"user":msg.author.id,"votes":1000,"currentBet":0})
            await msg.delete()



async def GameLobby(omsg):
    await Players.truncate()
    
    await client.wait_until_ready()
    global Searching
    global Running

    for i in range(60):
        await omsg.edit(content="Starting a game, everyone has "+str(60 -i)+" sec. to join!")
        await asyncio.sleep(1)

    await omsg.edit(content="Game Starts!")
    Searching = False
    Running = True
    
    MaxBet = 1
    Playerobj = Players.search(query.user >= 0)
    client.loop.create_task(calc()) # starting the calculation of some numbers
    
    msg = omsg
    omsg = None

    embed=discord.Embed(title="Auction", description="\u200b")
    embed.add_field(name="\u200b", value="Price: 100 Votes", inline=True)
    embed.add_field(name="Max Bet", value="All Bets", inline=True)

    await msg.edit(content="",embed=embed)
    await msg.channel.send("You can now Place your bet via dm, just msg a number")


async def calc():
    while not client.is_closed() and client.is_ready() and Running and not Searching:
        global AllBets
        Playerobj = Players.search(query.user >= 0)
        for Player in Playerobj:
            AllBets = int(AllBets) + int(Player["currentBet"])
        await asyncio.sleep(1)
        


client.run(config.token)