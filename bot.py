# bot.py
import os
import schedule
from datetime import datetime
from itertools import chain

import discord
from dotenv import load_dotenv
import json

# Loads our .env data
load_dotenv()
# Tokens for our bot and our server ID
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')
CHANNEL = os.getenv('MAIN_CHANNEL')
HELPCHANNEL = os.getenv('HELP_CHANNEL')

# Loads custom word banks for message monitoring
input_file = open('banks.json')
json_array = json.load(input_file)
wordVault = []
for bank in json_array:
    wordVault.append(bank)


# Sets up client as Discord client and pass it into the command handler #
client = discord.Client()

# Bot actions
###############################
# Actions performed on bot load
@client.event
async def on_ready():
    try:
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
    except Exception as e:
        print(e)
        with open('errors.log', 'a', newline=None) as r:
                r.write(f'{e} \n')

# Actions performed on member join
@client.event
async def on_member_join(member):
    joinMessage = f'Yo {member.name}, welcome'
    channel = ("CHANNEL_ID")
    await channel.send(joinMessage)

# Call and reponse actions
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    messageArr = message.content.lower().split(" ")

    # Search for the given phrase
    if message.content.lower() in chain(*wordVault):
        for bank in wordVault:
            if message.content.lower() in bank:
                index = wordVault.index(bank)
                targetBank = wordVault[index]
                await message.channel.send(file=discord.File(targetBank[-1]))

    # Search for individual words in the message
    elif(w in chain(*wordVault) for w in messageArr):
        for word in messageArr:
            if word in chain(*wordVault):
                for bank in wordVault:
                    if word in bank:
                        index = wordVault.index(bank)
                        targetBank = wordVault[index]
                        print(targetBank[-1])
                        await message.channel.send(file=discord.File(targetBank[-1]))
                        break

    # # Text response
    # if message.content.lower() == "this is a test of call and response":
    #     response = "This is a successful response"
    #     await message.channel.send(response)

    
    
    # Accepts and acknowledges requests for skills
    if message.channel.id == HELPCHANNEL:

        # Lists all requests made
        if message.content.lower() == "!requests":
            with open('request.log', 'r') as r:
                requests = list(r)
            await message.channel.send(f'Here\'s my current requests dawg:\n')
            for m in requests:
                await message.channel.send(f'{m}')
        # Adds datestamped and signed requests to the request log
        elif message.content[0] == "!":
            date = datetime.now()
            print(f'New request recieved')
            print(f'{message.content[1:]}')
            with open('request.log', 'a', newline=None) as r:
                r.write(f'{date} {message.author} - {message.content} \n')
            await message.channel.send('You got it king!')

# Scheduled events


# Error handling
@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)
