import os

from dotenv import load_dotenv


class BotUtils:
    def __init__(self, client):
        self.client = client
        load_dotenv()

    async def get_channel_users(self):
        szymek = await self.client.fetch_user(int(os.getenv('SZYMEK_ID')))
        macias = await self.client.fetch_user(int(os.getenv('MACIAS_ID')))
        bodzio = await self.client.fetch_user(int(os.getenv('BODZIO_ID')))
        wuja = await self.client.fetch_user(int(os.getenv('WUJA_ID')))
        return szymek, macias, bodzio, wuja

    async def get_user_by_id(self, id):
        return await self.client.fetch_user(id)

    async def get_text_channels(self):
        main_text_channel = await self.client.get_channel(int(os.getenv('MAIN_CHANNEL_ID')))
        return main_text_channel

    @staticmethod
    def get_token():
        return os.getenv('DISCORD_TOKEN')
