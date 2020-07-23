# bot.py
import json
import os
from itertools import chain
import asyncio

import discord
from dotenv import load_dotenv

import requests

# Loads our .env data
load_dotenv()
# Tokens for our bot and our server ID
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')
CHANNEL = os.getenv('MAIN_CHANNEL')
HELPCHANNEL = os.getenv('HELP_CHANNEL')



def check_valid_status_code(request):
    if request.status_code == 200:
        return request.json()

    return False


def get_joke():
    URL = 'https://official-joke-api.appspot.com/random_joke'
    request = requests.get(URL)
    data = check_valid_status_code(request)

    return data


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
    await client.get_channel(CHANNEL).send(joinMessage)

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
                response = targetBank[-1]
                # Checks to see if response is a string or a file, could lead to potential false positives, but it works for now so just let it
                if response[-4] == ".":
                    await message.channel.send(file=discord.File(response))
                else:
                    await message.channel.send(response)

    # Search for individual words in the message
    elif(w in chain(*wordVault) for w in messageArr):
        for word in messageArr:
            if word in chain(*wordVault):
                for bank in wordVault:
                    if word in bank:
                        index = wordVault.index(bank)
                        targetBank = wordVault[index]
                        response = targetBank[-1]
                        if response[-4] == ".":
                            await message.channel.send(file=discord.File(response))
                            break
                        else:
                            await message.channel.send(response)

    if "joke" in message.content.lower():
        joke = get_joke()
        print(joke)
        setup = joke['setup']
        await message.channel.send(f'{setup}')
        punchline =  joke['punchline']
        context = setup.replace('\'', ' ').split(" ")
        context = context[0].lower()
        print(context)

        if context in ["who", "what", "why", "when", "where", "how"]:
            print("if")
            print(f'message content:{message.content}')
            try:
                msg = await client.wait_for('message', timeout=5.0)
            except asyncio.TimeoutError:
                await message.channel.send(f'{punchline}')

            if context in msg.content.lower():
                await message.channel.send(f'{punchline}')
            else:
                await message.channel.send(f'No stupid: {punchline}')
        else:
            await message.channel.send(f'{punchline}')


    # Accepts and acknowledges requests for skills
    if message.channel.id == int(HELPCHANNEL):

        # Lists all requests made
        if message.content.lower() == "!requests":
            with open('request.log', 'r') as r:
                requests = list(r)
            await message.channel.send(f'Here\'s my current requests dawg:\n')
            for m in requests:
                await message.channel.send(f'{m}')
        # Adds date stamped and signed requests to the request log
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
