#!/usr/bin/env python

# bot.py: discord bot for organising games of MTG via discord servers
__author__ = "Matthe Dove"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Rob Knight"
__email__ = "matthew.dove13@gmail.com"
__status__ = "Development"

import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix='!')
lfg_fightqueue = []
@bot.command(name='lfg', help='Adds you too the fight queue')
async def look_to_fight(ctx):
    if not lfg_fightqueue:
        lfg_fightqueue.append(ctx.message.author.mention)
        queuedmessage = "Thanks {}, you have been added to the queue.".format(lfg_fightqueue[0])
        response = queuedmessage
    elif len(lfg_fightqueue) == 1:
        lfg_fightqueue.append(ctx.message.author.mention)
        fightmessage = "{} and {}... FIGHT.".format(lfg_fightqueue[0], lfg_fightqueue[1])
        response = fightmessage
        lfg_fightqueue.clear()
        
    await ctx.send(response)

@bot.command(name='leave', help='Leaves the queue')
async def look_to_fight(ctx):
    if ctx.message.author.mention in lfg_fightqueue:
        
        queuedmessage = "Thanks {}, you have been removed from.".format(lfg_fightqueue[0])
        lfg_fightqueue.remove(ctx.message.author.mention)
        response = queuedmessage
    else:
        fightmessage = "Quit yo fooling around, you ain't in this queue"
        response = fightmessage
        
    await ctx.send(response)

bot.run(TOKEN)
