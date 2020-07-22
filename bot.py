# bot.py
import os
import schedule
from datetime import datetime

import discord
from dotenv import load_dotenv
import json

# Loads our .env data
load_dotenv()
# Tokens for our bot and our server ID
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')
CHANNEL = os.getenv('MAIN_CHANNEL')

# Loads custom word banks for message monitoring
input_file = open('banks.json')
json_array = json.load(input_file)
wordBank = []
for bank in json_array:
    wordBank.append(bank)

client = discord.Client()

# Bot actions
###############################
# Actions performed on bot load
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


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
    # Text response
    if message.content.lower() == "this is a test of call and response":
        response = "This is a successful response"
        await message.channel.send(response)

    # Image response to word within sentence
    for word in wordBank[0]:
        if word in message.content.lower():  
            await message.channel.send(file=discord.File('reactions/ricardo1.gif'))
            break
    
    for word in wordBank[1]:
        if word in message.content.lower(): 
            await message.channel.send(file=discord.File('reactions/ricardo2.gif'))
            break
    
    if 'pizza' in message.content.lower():
        await message.channel.send(file=discord.File('reactions/pizza.gif'))

    # Image response to specific phrase
    if message.content.lower() == "can i get a hat wobble?":
        await message.channel.send(file=discord.File('reactions/hatwobble.gif'))
    
    # Accepts and acknowledges requests for skills
    if message.channel.id == 733424570136264726:

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
