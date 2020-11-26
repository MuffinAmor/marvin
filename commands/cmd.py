from datetime import datetime

import discord
from discord.ext import commands

from lib.request import request_setting

bot = commands.Bot(command_prefix='t!')

botcolor = 0x000ffc

bot.remove_command('help')

count = 0


class fight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command()
    async def support(self, ctx):
        if not ctx.author.bot:
            channel = self.bot.get_channel(638414867656736770)
            invitelinknew = await channel.create_invite(xkcd=True, max_age=600, reason="Neko Dev. Support")
            embed = discord.Embed(color=ctx.author.color)
            embed.add_field(name="Support Server Invite Link",
                            value="[Do you need help? Click me!]({})".format(invitelinknew))
            embed.set_footer(text='Message was requested by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
            embed.timestamp = datetime.utcnow()
            await ctx.channel.send(embed=embed)

    @bot.command()
    async def invite(self, ctx):
        if not ctx.author.bot:
            inv = "https://discordapp.com/api/oauth2/authorize?client_id=639955690835804170" \
                  "&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2FzHDxMNr&scope=bot"
            embed = discord.Embed(color=ctx.author.color)
            embed.add_field(name="Marvin Invite link", value="[Do you like invite me? Click here!]({})".format(inv))
            embed.set_footer(text='Do you need help? m!support', icon_url=ctx.author.avatar_url)
            embed.timestamp = datetime.utcnow()
            await ctx.channel.send(embed=embed)

    @bot.command()
    async def settings(self, ctx):
        server_id = str(ctx.guild.id)
        coins_per_msg = request_setting(server_id, 'coins_per_message')
        coins_per_voice = request_setting(server_id, 'coins_per_voice')
        delay = request_setting(server_id, 'time_delay')
        embed = discord.Embed(title="Server Settings:",
                              description="Coins per Message: {}\n"
                                          "Coins per Voice Minute: {}\n"
                                          "Gather Delay: {} sec".format(coins_per_msg, coins_per_voice, delay))
        embed.set_footer(text='Do you need help? m!support', icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(fight(bot))
