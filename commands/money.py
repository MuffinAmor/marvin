from discord.ext import commands
import discord

from lib.request import request_user_stats

bot = commands.Bot(command_prefix='m!')

botcolor = 0x000ffc

bot.remove_command('help')


class MoneyClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx, member:discord.Member=None):
        member = member or ctx.author
        server_id = str(ctx.guild.id)
        user_id = str(member.id)
        balance = request_user_stats(server_id, user_id, 'money')
        embed = discord.Embed(title="Your Profile",
                              description="Your Coins: {}".format(balance))
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MoneyClass(bot))
