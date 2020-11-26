import asyncio
from datetime import datetime

import discord
from discord.ext import commands

from lib.create import create_ticket, create_ticket_group
from lib.delete import delete_ticket, delete_group
from lib.edit import set_category, set_message, set_count, set_log
from lib.request import request_category, request_name_message, request_ticket, request_channel, \
    request_name_channel, request_log, request_groups

bot = commands.Bot(command_prefix='m!')

botcolor = 0x000ffc

bot.remove_command('help')


class ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def delete_ticket_group(self, ctx, *args: str):
        server_id = str(ctx.guild.id)
        msg = ' '.join(args)
        if not msg:
            await ctx.send("Please tell me the Groupname first.")
        else:
            await ctx.send(delete_group(server_id, msg))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def create_ticket_group(self, ctx, *args: str):
        msg = ' '.join(args)
        if not msg:
            await ctx.send("Please tell me the Groupname first.")
        else:
            server_id = str(ctx.guild.id)
            await ctx.send(create_ticket_group(server_id, msg))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_log(self, ctx, channel: discord.TextChannel, *args: str):
        server_id = str(ctx.guild.id)
        msg = ' '.join(args)
        if not channel:
            await ctx.send('Please tell me the Channel first.')
        elif not request_groups(server_id, 'single', msg):
            await ctx.send("This Ticketgroup not exist.")
        elif not msg:
            await ctx.send('Please tell me the Groupname first.')
        else:
            server_id = str(ctx.guild.id)
            set_log(server_id, msg, str(channel.id))
            await ctx.send('The Channel **{}** has been setted as LOG.'.format(channel.name))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_category(self, ctx, category: discord.CategoryChannel, *args: str):
        server_id = str(ctx.guild.id)
        msg = ' '.join(args)
        if not category:
            await ctx.send('Please tell me a Category first.')
        elif not request_groups(server_id, 'single', msg):
            await ctx.send("This Ticketgroup not exist.")
        elif not msg:
            await ctx.send('Please tell me the Groupname first.')
        else:
            server_id = str(ctx.guild.id)
            set_category(server_id, msg, str(category.id))
            await ctx.send('The Category **{}** has been setted.'.format(category.name))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def activ_ticket(self, ctx, *args: str):
        msg = ' '.join(args)
        server_id = str(ctx.guild.id)
        if not msg:
            await ctx.send("Please tell me Ticketgroup")
        elif not request_groups(server_id, 'single', msg):
            await ctx.send("This Ticketgroup not exist.")
        elif not request_category(server_id, msg):
            await ctx.send("Please set a Ticket Group Category first.")
        else:
            embed = discord.Embed(color=discord.Color.dark_blue())
            embed.set_author(name="{}".format(msg), icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Create here your Ticket.", value="Click here to create your Ticket")
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            message = await ctx.send(embed=embed)
            set_message(server_id, msg, str(message.id))
            reaction = self.bot.get_emoji(704706438009847838)
            await message.add_reaction(str(reaction))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticketgroups(self, ctx):
        server_id = str(ctx.guild.id)
        embed = discord.Embed(title="The Ticket-Groups on this Server:",
                              description=request_groups(server_id, 'liste'))
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.member.bot:
            server_id = str(payload.guild_id)
            server = self.bot.get_guild(int(server_id))
            message_id = str(payload.message_id)
            cha = str(payload.channel_id)
            name_text = request_name_message(server_id, message_id)
            name_text2 = request_name_channel(server_id, cha)
            if name_text:
                name = name_text.replace(".json", "")
            elif name_text2:
                name = name_text2.replace(".json", "")
            else:
                name = None
            if name:
                open_ticket_emote = self.bot.get_emoji(704706438009847838)
                emote1 = self.bot.get_emoji(656148810527145997)
                emote2 = self.bot.get_emoji(656148884124598272)
                if payload.emoji == open_ticket_emote:
                    count = request_ticket(server_id, name)
                    category_id = request_category(server_id, name)
                    for i in payload.member.guild.categories:
                        if str(i.id) == category_id:
                            channel = await payload.member.guild.create_text_channel(name="ticket-{}".format(count),
                                                                                     category=i)
                            await channel.set_permissions(payload.member, send_messages=True, read_messages=True)
                            await channel.set_permissions(server.default_role, read_messages=False)
                            create_ticket(server_id, name, str(channel.id))
                            set_count(server_id, name)
                            embed = discord.Embed(color=discord.Color.dark_blue())
                            embed.add_field(name="Welcome", value="Use {} to save the ticket\n"
                                                                  "Use 🔒 to close or reopen the Ticket\n"
                                                                  "Use {} to delete the Ticket.".format(emote1, emote2))
                            embed.set_author(name=name)
                            message = await channel.send(payload.member.mention, embed=embed)
                            for _ in server.channels:
                                if _.type == discord.ChannelType.text:
                                    try:
                                        msg = await _.fetch_message(payload.message_id)
                                    except:
                                        msg = None
                                    if msg is not None:
                                        await msg.remove_reaction(open_ticket_emote, payload.member)
                                        break
                            await message.add_reaction(emote1)
                            await message.add_reaction("🔒")
                            await message.add_reaction(emote2)
                            log_id = request_log(server_id, name)
                            log = self.bot.get_channel(int(log_id))
                            if log:
                                embed = discord.Embed(title="Ticket Open!",
                                                      description="Ticket **{}** \n"
                                                                  "in Ticketgroup **{}** \n"
                                                                  "open by **{}**".format(
                                                          int(count), name, payload.member))
                                embed.timestamp = datetime.utcnow()
                                await log.send(embed=embed)
                            return
                elif str(payload.emoji) == str("🔒"):
                    channel = self.bot.get_channel(payload.channel_id)
                    if channel:
                        if "ticket" in channel.name:
                            await channel.edit(name=channel.name.replace("ticket", "closed"))
                            await channel.set_permissions(payload.member, send_messages=False, read_messages=False)
                            log_id = request_log(server_id, name)
                            log = self.bot.get_channel(int(log_id))
                            if log:
                                if "ticket" in channel.name:
                                    chan = channel.name.replace("ticket-", "")
                                elif "closed" in channel.name:
                                    chan = channel.name.replace("closed-", "")
                                else:
                                    chan = "Undefinied"
                                embed = discord.Embed(title="Ticket closed!",
                                                      description="Ticket **{}** \n"
                                                                  "in Ticketgroup **{}** \n"
                                                                  "reopen by **{}**".format(
                                                          chan, name,
                                                          payload.member))
                                embed.timestamp = datetime.utcnow()
                                await log.send(embed=embed)
                            return
                        elif "closed" in channel.name:
                            await channel.edit(name=channel.name.replace("closed", "ticket"))
                            await channel.set_permissions(payload.member, send_messages=True, read_messages=True)
                            log_id = request_log(server_id, name)
                            log = self.bot.get_channel(int(log_id))
                            if log:
                                if "ticket" in channel.name:
                                    chan = channel.name.replace("ticket-", "")
                                elif "closed" in channel.name:
                                    chan = channel.name.replace("closed-", "")
                                else:
                                    chan = "Undefinied"
                                embed = discord.Embed(title="Ticket reopen!",
                                                      description="Ticket **{}** \n"
                                                                  "in Ticketgroup **{}** \n"
                                                                  "closed by **{}**".format(
                                                          chan, name,
                                                          payload.member))
                                embed.timestamp = datetime.utcnow()
                                await log.send(embed=embed)
                            return
                elif payload.emoji == emote1:
                    if payload.member.guild_permissions.administrator:
                        channelids = request_channel(server_id, name)
                        for i in channelids:
                            channel = self.bot.get_channel(int(i))
                            if channel:
                                if "ticket" in channel.name:
                                    await channel.edit(name=channel.name.replace("ticket", "saved"))
                                    await channel.set_permissions(payload.member, send_messages=False,
                                                                  read_messages=False)
                                    delete_ticket(server_id, name, str(payload.channel_id))
                                    message = await self.bot.get_channel(payload.channel_id).fetch_message(
                                        payload.message_id)
                                    await message.remove_reaction(emote1, self.bot.user, )
                                    await channel.send("Ticket saved. Reaction actions disabled.")
                                    log_id = request_log(server_id, name)
                                    log = self.bot.get_channel(int(log_id))
                                    if log:
                                        if "ticket" in channel.name:
                                            chan = channel.name.replace("ticket-", "")
                                        elif "closed" in channel.name:
                                            chan = channel.name.replace("closed-", "")
                                        else:
                                            chan = "Undefinied"
                                        embed = discord.Embed(title="Ticket saved!",
                                                              description="Ticket **{}** \n"
                                                                          "in Ticketgroup **{}** \n"
                                                                          "saved by **{}**".format(
                                                                  chan, name,
                                                                  payload.member))
                                        embed.timestamp = datetime.utcnow()
                                        await log.send(embed=embed)
                                    return
                                elif "closed" in channel.name:
                                    await channel.edit(name=channel.name.replace("closed", "ticket"))
                                    await channel.set_permissions(payload.member, send_messages=False,
                                                                  read_messages=False)
                                    delete_ticket(server_id, name, str(payload.channel_id))
                                    message = await self.bot.get_channel(payload.channel_id).fetch_message(
                                        payload.message_id)
                                    await message.remove_reaction(emote1, self.bot.user)
                                    await channel.send("Ticket saved. Reaction actions disabled.")
                                    log_id = request_log(server_id, name)
                                    log = self.bot.get_channel(int(log_id))
                                    if log:
                                        if "ticket" in channel.name:
                                            chan = channel.name.replace("ticket-", "")
                                        elif "closed" in channel.name:
                                            chan = channel.name.replace("closed-", "")
                                        else:
                                            chan = "Undefinied"
                                        embed = discord.Embed(title="Ticket saved!",
                                                              description="Ticket **{}** \n"
                                                                          "in Ticketgroup **{}** \n"
                                                                          "saved by **{}**".format(
                                                                  chan, name,
                                                                  payload.member))
                                        embed.timestamp = datetime.utcnow()
                                        await log.send(embed=embed)
                                    return
                elif payload.emoji == emote2:
                    channelids = request_channel(server_id, name)
                    for i in channelids:
                        channel = self.bot.get_channel(int(i))
                        if channel:
                            if channel.id == payload.channel_id:
                                del_channel = self.bot.get_channel(payload.channel_id)
                                await del_channel.send("Das Ticket wird in 5 Sekunden gelöscht.")
                                await asyncio.sleep(5)
                                await del_channel.delete()
                                delete_ticket(server_id, name, str(payload.channel_id))
                                log_id = request_log(server_id, name)
                                log = self.bot.get_channel(int(log_id))
                                if log:
                                    if "ticket" in channel.name:
                                        chan = channel.name.replace("ticket-", "")
                                    elif "closed" in channel.name:
                                        chan = channel.name.replace("closed-", "")
                                    else:
                                        chan = "Undefinied"
                                    embed = discord.Embed(title="Ticket Delete!",
                                                          description="Ticket **{}** \n"
                                                                      "in Ticketgroup **{}** \n"
                                                                      "deleted by **{}**".format(chan, name,
                                                                                                 payload.member))
                                    embed.timestamp = datetime.utcnow()
                                    await log.send(embed=embed)
                                return


def setup(bot):
    bot.add_cog(ticket(bot))
