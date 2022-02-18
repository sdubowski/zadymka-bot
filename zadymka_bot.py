import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_voice_state_update(member, before, after):
    if member == client.user:
        return

    wuja = await client.fetch_user(os.getenv('WUJA_ID'))
    message_channel = client.get_channel(os.getenv('502237152604717078'))
    if before.channel is None and after.channel is not None and member == wuja:
        wuja_response = '<@' + f'{wuja.id}' + '>' + ' Siema wujek niezła honda'
        for i in range(4):
            await message_channel.send(wuja_response)
        await message_channel.send(file=discord.File('./resources/honda.gif'))
        return

    if before.channel is None and after.channel is not None:
        await message_channel.send("elo kurwa", tts=True)
        return


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    szymek = await client.fetch_user(os.getenv('SZYMEK_ID'))
    macias = await client.fetch_user(os.getenv('MACIAS_ID'))
    bodzio = await client.fetch_user(os.getenv('BODZIO_ID'))
    wuja = await client.fetch_user(os.getenv('WUJA_ID'))

    szymek_response = '<@'+f'{szymek.id}' +'>' +' Szymek koks'
    macias_response = '<@'+f'{macias.id}' +'>' +' Macias kocur'
    bodzio_respone = '<@'+f'{bodzio.id}' +'>' + ' Wydupiaj na pole es'
    wuja_response = '<@'+f'{wuja.id}' +'>' + ' <3'

    beta_message = '.play https://www.youtube.com/watch?v=edVgkrF92M8'

    not_link = beta_message != message.content
    if not_link and message.author == szymek:
        response = szymek_response
        await message.channel.send(response)
        return

    if not_link and message.author == macias:
        response = macias_response
        await message.channel.send(response)
        return

    if not_link and message.author == bodzio:
        for i in range(3):
            response = bodzio_respone
            await message.channel.send(response)
        await message.channel.send(file=discord.File('./resources/tractor.gif'))
        return

    if not_link and message.author == wuja:
        response = wuja_response
        await message.channel.send(response)
        return

    if not not_link:
        await message.channel.send(file=discord.File('./resources/diho.gif'))
        return

client.run(TOKEN)
