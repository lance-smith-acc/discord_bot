# bot.py
import os
import schedule
import time

import discord
from dotenv import load_dotenv

# Loads our .env data
load_dotenv()
# Tokens for our bot and our server ID
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')
CHANNEL = os.getenv('MAIN_CHANNEL')

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
    joinMessage = f'Yo {member.name}'
    channel = member.get_channel("CHANNEL_ID")
    await channel.send(joinMessage)

# Call and reponse actions
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    word_bank = [
        'Test1', 'Test2', 'Test3', 'Test4'
    ]

    # Text response
    if message.content.lower() == "this is a test of call and response":
        response = "This is a successful response"
        await message.channel.send(response)
    
    # Image response to word within sentence
    for word in word_bank:
        if word in message.content.lower():
            await message.channel.send(file=discord.File('ricardo1.gif'))
            break

    # Image response to specific phrase
    if message.content.lower() == "can i get a hat wobble?":
        await message.channel.send(file=discord.File('hatwobble.gif'))

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