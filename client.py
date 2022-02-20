import os

import discord
from dotenv import load_dotenv


class Client:

    def __init__(self):
        self.szymek = await client.fetch_user(os.getenv('SZYMEK_ID'))
        self.macias = await client.fetch_user(os.getenv('MACIAS_ID'))
        self.bodzio = await client.fetch_user(os.getenv('BODZIO_ID'))
        self.wuja = await client.fetch_user(os.getenv('WUJA_ID'))
        self.main_text_channel = await client.get_channel(os.getenv('502237152604717078'))

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    client = discord.Client()

    @client.event
    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_voice_state_update(self, member, before, after):
        if member == client.user:
            return

        if before.channel is None and after.channel is not None and member == self.wuja:
            wuja_response = '<@' + f'{wuja.id}' + '>' + ' Siema wujek niezła honda'
            for i in range(4):
                await message_channel.send(wuja_response)
            await message_channel.send(file=discord.File('./resources/honda.gif'))
            return

        if before.channel is None and after.channel is not None:
            await message_channel.send("elo kurwa", tts=True)
            return

    @client.event
    async def on_message(self, message):
        if message.author == client.user:
            return

        szymek_response = '<@' + f'{szymek.id}' + '>' + ' Szymek koks'
        macias_response = '<@' + f'{macias.id}' + '>' + ' Macias kocur'
        bodzio_respone = '<@' + f'{bodzio.id}' + '>' + ' Wydupiaj na pole es'
        wuja_response = '<@' + f'{wuja.id}' + '>' + ' <3'

        szampan = '.play https://www.youtube.com/watch?v=edVgkrF92M8'

        display_diho = szampan == message.content
        if not display_diho and message.author == self.szymek:
            response = szymek_response
            await message.channel.send(response)
            return

        if not display_diho and message.author == self.macias:
            response = macias_response
            await message.channel.send(response)
            return

        if not display_diho and message.author == self.bodzio:
            for i in range(3):
                response = bodzio_respone
                await message.channel.send(response)
            await message.channel.send(file=discord.File('./resources/tractor.gif'))
            return

        if not display_diho and message.author == self.wuja:
            response = wuja_response
            await message.channel.send(response)
            return

        if display_diho:
            await message.channel.send(file=discord.File('./resources/diho.gif'))
            return

    client.run(TOKEN)
