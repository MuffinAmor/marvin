from datetime import datetime

import discord
from discord.ext import commands

from lib.edit import edit_user_stats, edit_setting
from lib.request import request_user_stats
from lib.shop import add_market_item, create_market_UI, remove_market_item, get_info

bot = commands.Bot(command_prefix='.')

botcolor = 0x00ff06

bot.remove_command('help')


class ItemShop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = 0

    @commands.command()
    async def shop(self, ctx):
        UI = create_market_UI(str(ctx.guild.id), self.count)
        if UI is None:
            self.count = 0
            UI = create_market_UI(str(ctx.guild.id), self.count)
        embed = discord.Embed(title="Role Market",
                              color=ctx.author.color)
        embed.add_field(name="We have:", value=UI,
                        inline=False)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text="Market", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url="https://neko-dev.de/imgstore/shop.gif")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("◀️")
        await msg.add_reaction("▶️")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.author.id == self.bot.user.id:
            if not user.bot:
                server_id = user.guild.id
                if reaction.emoji == "▶️":
                    self.count += 1
                    UI = create_market_UI(str(server_id), self.count)
                    if UI is None:
                        await reaction.message.remove_reaction("▶️", user)
                    else:
                        embed = discord.Embed(title="Role Market",
                                              color=user.color)
                        embed.add_field(name="We have:", value=UI,
                                        inline=False)
                        embed.timestamp = datetime.utcnow()
                        embed.set_footer(text="Market", icon_url=self.bot.user.avatar_url)
                        embed.set_thumbnail(url="https://neko-dev.de/imgstore/shop.gif")
                        await reaction.message.edit(embed=embed)
                        await reaction.message.remove_reaction("▶️", user)
                if reaction.emoji == "◀️":
                    self.count -= 1
                    UI = create_market_UI(str(server_id), self.count)
                    if UI is None:
                        await reaction.message.remove_reaction("◀️", user)
                    else:
                        embed = discord.Embed(title="Role Market",
                                              color=user.color)
                        embed.add_field(name="We have:", value=UI,
                                        inline=False)
                        embed.timestamp = datetime.utcnow()
                        embed.set_footer(text="Market", icon_url=self.bot.user.avatar_url)
                        embed.set_thumbnail(url="https://neko-dev.de/imgstore/shop.gif")
                        await reaction.message.edit(embed=embed)
                        await reaction.message.remove_reaction("◀️", user)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_role(self, ctx, role: discord.Role, number: int):
        if not role:
            await ctx.send("It looks like that you forgot to enter a Role.")
        elif not number:
            await ctx.send("It looks like that you forgot to enter a Price for the Role.")
        else:
            server_id = str(ctx.guild.id)
            role_name = role.name
            role_id = role.id
            try:
                price = int(number)
            except TypeError:
                await ctx.send("It looks like that you forgot to enter a Price for the Role.")
                return
            await ctx.send(add_market_item(server_id, role_name, role_id, price))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_role(self, ctx, role: discord.Role = None):
        if not role:
            await ctx.send("Please enter a Role.")
        else:
            server_id = str(ctx.guild.id)
            role_id = str(role.id)
            await ctx.send(remove_market_item(server_id, role_id))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_delay(self, ctx, time: int):
        if not time:
            await ctx.send("Please give me the delay time in seconds!")
        else:
            server_id = str(ctx.guild.id)
            edit_setting(server_id, 'time_delay', round(time))
            await ctx.send("The Coin delay has been setted to {} seconds".format(time))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_msg_coins(self, ctx, coins: int):
        if not coins:
            await ctx.send("Please tell me the amount of coins per Message.")
        else:
            server_id = str(ctx.guild.id)
            edit_setting(server_id, 'coins_per_message', round(coins))
            await ctx.send("The Coins per Message has been setted to {}".format(coins))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_voice_coins(self, ctx, coins: int):
        if not coins:
            await ctx.send("Please tell me the amount of coins per Minute.")
        else:
            server_id = str(ctx.guild.id)
            edit_setting(server_id, 'coins_per_voice', round(coins))
            await ctx.send("The Coins per Minute in a Voice has been setted to {}".format(coins))

    @commands.command()
    async def buy(self, ctx, role: discord.Role = None):
        if not role:
            await ctx.send("Please enter the Role")
        else:
            token = str(role.id)
            server_id = str(ctx.guild.id)
            user_id = str(ctx.author.id)
            preis = get_info(server_id, token, 'Preis')
            if preis:
                RoleId = get_info(server_id, token, 'RollenID')
                MemberMoney = request_user_stats(server_id, user_id, 'money')
                if MemberMoney < preis:
                    await ctx.send("It looks like, that you have not enough Money.")
                else:
                    role = ctx.guild.get_role(RoleId)
                    if role:
                        if role not in ctx.author.roles:
                            try:
                                await ctx.author.add_roles(role)
                            except PermissionError:
                                await ctx.send("Sorry, but i have not enough permissions to give you the Role.")
                            else:
                                edit_user_stats(server_id, user_id, 'money', MemberMoney - preis)
                                await ctx.send("Congrats, you have buy the Role: {}".format(role))
                        else:
                            await ctx.send("It looks like that you have allready the Role!")
                    else:
                        await ctx.send("This Role is not avaible anymore!\n"
                                       "Ill remove it from the Shop.")
                        await ctx.send(remove_market_item(server_id, token))

            else:
                await ctx.send("Ops, i don't found a Role. Please check the Key.")


def setup(bot):
    bot.add_cog(ItemShop(bot))
