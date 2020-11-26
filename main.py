import asyncio
import os

import discord
from discord.ext import commands

TOKEN = ''

bot = commands.Bot(command_prefix='m!')

botcolor = 0xffffff

bot.remove_command('help')

os.chdir(r'/home/niko/data/Marvin')
########################################################################################################################

extensions = ['commands.cmd', 'commands.auto', 'commands.ticket', 'commands.help', 'commands.dbl', 'commands.money',
              'commands.shop']


@bot.event
async def on_ready():
    print('--------------------------------------')
    print('Bot is ready.')
    print('Eingeloggt als')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------------------------')
    await status_task()


########################################################################################################################
async def status_task():
    await bot.change_presence(activity=discord.Game('m!help | Marvin'))
    # await bot.change_presence(activity=discord.Game('Maininstance'),
    #                          status=discord.Status.idle)
    ########################################################################################################################


@bot.command()
@commands.is_owner()
async def goodnight(ctx):
    await ctx.channel.send("Sleep well")
    await bot.logout()


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(extension)
        print('{} wurde geladen.'.format(extension))
        embed = discord.Embed(
            title='{} wurde geladen.'.format(extension),
            color=botcolor
        )
        msg = await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await msg.delete()
    except Exception as error:
        print('{} konnte nicht geladen werden. [{}]'.format(extension, error))
        embed = discord.Embed(
            title='{} konnte nicht geladen werden. [{}]'.format(extension, error),
            color=botcolor
        )
        msg = await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await msg.delete()


########################################################################################################################
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(extension)
        print('{} wurde deaktiviert.'.format(extension))
        embed = discord.Embed(
            title='{} wurde deaktiviert.'.format(extension),
            color=botcolor
        )
        msg = await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await msg.delete()
    except Exception as error:
        print('{} konnte nich deaktiviert werden. [{}]'.format(extension, error))
        embed = discord.Embed(
            title='{} konnte nicht deaktiviert werden. [{}]'.format(extension, error),
            color=botcolor
        )
        msg = await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await msg.delete()


########################################################################################################################
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        bot.unload_extension(extension)
        bot.load_extension(extension)
        await ctx.channel.send('{} wurde neu geladen.'.format(extension))
    except Exception as error:
        await ctx.channel.send('{} konnte nicht geladen werden. [{}]'.format(extension, error))


########################################################################################################################
if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} konnte nicht geladen werden. [{}]'.format(extension, error))

bot.run(TOKEN)
