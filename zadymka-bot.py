import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.music_bot import MusicBot
from services.utils import BotUtils

load_dotenv()

bot = commands.Bot(command_prefix='!')
utils = BotUtils(bot)
token = utils.get_token()
bot.add_cog(MusicBot(bot))


@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command(pass_context=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command(pass_context=True)
async def rolnik(ctx):
    await ctx.send(file=discord.File('./resources/banner.txt'))


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return
    szymek, macias, bodzio, wuja = await utils.get_channel_users()
    if member == bodzio:
        if after.mute:
            text_channel = utils.get_text_channels()
            await text_channel.send("Masz gembe pełną śmieci", tts=True)
            await text_channel.send(file=discord.File('./resources/GarbageMonster.jpg'))

    current_members = list()
    voice_states = list()

    for voice_channel in member.guild.voice_channels:
        if len(voice_channel.voice_states) > 0:
            for states in voice_channel.voice_states:
                voice_states.append(states)

        if len(voice_channel.members) > 0:
            for channel_member in voice_channel.members:
                current_members.append(channel_member)

    if len(voice_states) == 1:
        bot_member = next(filter(lambda x: x == bot.user, current_members))
        if bot_member is not None:
            await leave(bot_member.guild)




@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content[0] == '!':
        await bot.process_commands(message)
        return

    szymek, macias, bodzio, wuja = await utils.get_channel_users()
    bodzio_respone = '<@' + f'{bodzio.id}' + '>' + ' Wydupiaj na pole es'

    szampan = '.play https://www.youtube.com/watch?v=edVgkrF92M8'

    display_diho = szampan == message.content

    if not display_diho:

        if message.author == bodzio:
            for i in range(3):
                response = bodzio_respone
                await message.channel.send(response)
            await message.channel.send(file=discord.File('./resources/tractor.gif'))
            return

    else:
        await message.channel.send(file=discord.File('./resources/diho.gif'))
        return


bot.run(token)
