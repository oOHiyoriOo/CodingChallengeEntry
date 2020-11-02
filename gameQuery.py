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
AcceptDM = False
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

    global Searching
    global Running
    global AcceptDM
    
    if msg.author.id == client.user.id:
        return

    elif msg.content == "*start" and not Running and not Searching:
        Players.truncate()
        Players.insert({"user":msg.author.id,"votes":1000,"currentBet":0})
        omsg = await msg.channel.send("Starting a game, everyone has 60 sec. to join!")
        Searching = True
        await msg.delete()
        await GameLobby(omsg)


    elif msg.content == "*join" and not Running and Searching:
        if not msg.author.id in Players:
            Players.insert({"user":msg.author.id,"votes":1000,"currentBet":0})
        await msg.delete()



    elif msg.channel.type is discord.ChannelType.private and AcceptDM:
        try:
            bet = int(msg.content)
            if bet <= int(Players.search(query.user == msg.author.id)[0]['votes']):
                Players.update({"currentBet":bet})
                await msg.channel.send("Placed your bet of: "+str(bet))
            else:
                await msg.channel.send("you dont have enough votes to purchase this")
        except:
            await msg.channel.send("Cant place a bet with value: "+str(msg.content))

    # elif isinstance(msg.channel, discord.channel.DMChannel) and AcceptDM:
    #     try:
    #         bet = int(msg.content)
    #         if bet <= int(Players.search(query.user == msg.author.id)[0]['votes']):
    #             Players.update({"currentBet":bet})
    #             await msg.channel.send("Placed your bet of: "+str(bet))
    #         else:
    #             await msg.channel.send("you dont have enough votes to purchase this")
    #     except:
    #         await msg.channel.send("Cant place a bet with value: "+str(msg.content))
    
    else:
        warn(str(msg.channel.type))

async def GameLobby(omsg):
    await client.wait_until_ready()
    global Searching
    global Running
    global AcceptDM


    for i in range(10):
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
    embed.add_field(name="0", value="0", inline=True)

    await msg.edit(content="",embed=embed)
    await msg.channel.send("You can now Place your bet via dm, for 60 seconds")^
    client.loop.create_task(UpdateEmbed())
    AcceptDM = True



async def calc():
    while not client.is_closed() and client.is_ready() and Running and not Searching:
        global AllBets
        Playerobj = Players.search(query.user >= 0)
        for Player in Playerobj:
            AllBets = int(AllBets) + int(Player["currentBet"])
        await asyncio.sleep(1)
        
async def UpdateEmbed(msg):
    while not client.is_closed() and client.is_ready() and Running and not Searching:
        embed=discord.Embed(title="Auction", description="\u200b")
        embed.add_field(name="\u200b", value="Price: 100 Votes", inline=True)
        embed.add_field(name="0", value=str(AllBets), inline=True)
        msg.edit(embed=embed)
        await asyncio.sleep(1)

client.run(config.token)