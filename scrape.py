import discord
import asyncio
import os
import datetime as dt
import json
import asyncio
from discord.ext import commands
import random
from datetime import datetime
import numpy
import configparser
import operator
from string import punctuation
import os

class ShortMessage(object):
    def __init__(self, message = None):
        self.author = message.author.name
        self.id = message.author.id
        self.content = message.content
        self.time = (message.timestamp.timestamp())

description = 'Daniel Bot: By Daniel'
bot = commands.Bot(command_prefix='?', description=description)

#Run on bot start
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(game=discord.Game(name='?help - Downdating...'))

    channels = bot.get_all_channels()

    for x in bot.voice_clients:
        await x.disconnect()

    #Logs all messages in all channels into channel specific text files
    for x in channels:
        

        fn = os.path.join(os.path.dirname(__file__), 'Logs', str(x.id) + '.json')

        with open(fn, "w+", encoding = 'utf8') as f:
            l = []
            
            counter = 0
            async for message in bot.logs_from(x, limit=999999999):

                d = {"author" : '', "author_id" : '', "content" : '', "time" : ''}

                if counter % 1000 == 0:
                    print ("Logging channel: " + str(x.id) + ' [' + str(counter) + ']')

                counter += 1
                d["author"] = message.author.name
                d["author_id"] = str(message.author.id)
                d["content"] = message.content
                d["time"] = str(message.timestamp.timestamp())
                l.append(d)
                #if counter > 10000:
                #    break
                #print(str(d))

            json.dump(l, f)

        print(str(datetime.now())+ ' -> Channel logged: ' + x.id)

    await bot.change_presence(game=discord.Game(name='?help'))

config = configparser.ConfigParser()
config.read('config.ini')
cfg = config['SETTINGS']
token = cfg['token']

bot.run(token)