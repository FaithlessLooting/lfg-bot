#!/usr/bin/env python

# bot.py: discord bot for organising games of MTG via discord servers
__author__ = "Matthe Dove"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Rob Knight"
__email__ = "matthew.dove13@gmail.com"
__status__ = "Development"

import os
import re
import discord
from dotenv import load_dotenv
from discord.ext import commands
import sqlite3
import pandas as pd
from pandas import DataFrame

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix='!')
lfg_fightqueue = []
lfg_leaguequeue = []
current_fights = []
@bot.command(name='lfg', help='Adds you o the fight queue')
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
async def leave_fight(ctx):
    if ctx.message.author.mention in lfg_fightqueue:

        queuedmessage = "Thanks {}, you have been removed from.".format(lfg_fightqueue[0])
        lfg_fightqueue.remove(ctx.message.author.mention)
        response = queuedmessage
    else:
        fightmessage = "Quit yo fooling around, you ain't in this queue"
        response = fightmessage

    await ctx.send(response)

@bot.command(name='joinleague', help='Joins Monthly League')
async def joinleague(ctx):
        conn = sqlite3.connect('lfgbot.db')
        c = conn.cursor()
        author=ctx.message.author.mention
        author = re.sub('[<>]', '', author)
        authorid=ctx.message.author.id
        print(author)
        print(authorid)
        authorid=str(authorid)
        author=str(author)
        # Insert a row of data
        c.execute("INSERT INTO users VALUES ("+authorid+",'"+author+"',"+"0"+")")

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()
        queuedmessage = "Thanks {}, you have been registered for the monthly league.".format(ctx.message.author.mention)
        response = queuedmessage
        await ctx.send(response)

@bot.command(name='leaguequeue', help='Joins Monthly League queue')
async def joinleaguequeue(ctx):
    conn = sqlite3.connect('lfgbot.db')
    c = conn.cursor()
    author=ctx.message.author.mention
    authorid=ctx.message.author.id
    authorid=str(authorid)
    author=str(author)
    c.execute("select User_ID, User_Name, Score from users where User_ID = '"+authorid+"'")

    for row in c.fetchall():
        User_ID, User_Name, Score = row
        print('{} {} {}'.format(
            User_ID, User_Name, Score))
    if not lfg_leaguequeue:
        lfg_leaguequeue.append(ctx.message.author.mention)
        queuedmessage = "Thanks {}, you have been added to the queue.".format(lfg_leaguequeue[0])
        response = queuedmessage
    elif len(lfg_leaguequeue) == 1:
        lfg_leaguequeue.append(ctx.message.author.mention)
        fightmessage = "{} and {}... FIGHT. Please report your result by the victor typing !winner, currently this is an honor based system, please message a mod if you feel a player is cheating".format(lfg_leaguequeue[0], lfg_leaguequeue[1])
        current_fights.append(lfg_leaguequeue[0]+"-"+lfg_leaguequeue[1])
        response = fightmessage
        lfg_leaguequeue.clear()
        print(current_fights[0])
    await ctx.send(response)
@bot.command(name='winner', help='reports league winner')
async def winner(ctx):
    if current_fights:
        conn = sqlite3.connect('lfgbot.db')
        c = conn.cursor()
        author=ctx.message.author.mention
        authorid=ctx.message.author.id
        authorid=str(authorid)
        author=str(author)
        c.execute("select User_ID, User_Name, Score from users where User_ID = '"+authorid+"'")
        for row in c.fetchall():
            User_ID, User_Name, Score = row
            print('{} {} {}'.format(
                User_ID, User_Name, Score))
            OldScore = Score
            print(OldScore)
        c.close()
        for i in current_fights:
            if authorid in i:
                NewScore= OldScore+3
                NewScore = str(NewScore)
                print(NewScore)
                print(authorid)
                conn = sqlite3.connect('lfgbot.db')
                c = conn.cursor()
                c.execute("UPDATE users SET Score = "+NewScore+" WHERE User_ID = "+authorid)
                conn.commit()
                current_fights.remove(i)
                c.close()
                queuedmessage = "Thanks {}, your result has been confirmed.".format(ctx.message.author.mention)
                response = queuedmessage
            else:
                queuedmessage = "Sorry {}, no matches found for you.".format(ctx.message.author.mention)
                response = queuedmessage
    else:
         queuedmessage = "Error: Queue Empty"
         response = queuedmessage
    await ctx.send(response)

bot.run(TOKEN)
