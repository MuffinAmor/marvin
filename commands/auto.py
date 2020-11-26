from datetime import datetime
from time import time

import discord
from discord.ext import commands

from lib.create import create_server, create_user
from lib.delete import delete_ticket, delete_server
from lib.edit import set_category, set_message, edit_user_stats
from lib.request import request_name_channel, request_name_category, request_name_message, request_user_stats, \
    request_setting
from lib.temp import set_join_time, delete_temp_user, request_join_time

bot = commands.Bot(command_prefix='t!')

botcolor = 0x000ffc

bot.remove_command('help')


class auto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter = 0

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            server = self.bot.get_guild(382290709249785857)
            try:
                inv = await server.invites()
            except:
                pass
            for invites in inv:
                if invites:
                    invite2 = invites.url
                    break
            else:
                invite2 = "https://discord.gg"
            self.counter = + 1
            channel = self.bot.get_channel(692781515045601402)
            await channel.send("*{}* keeps a error ```{}```".format(ctx.message.content, error))
            embed = discord.Embed(title="Ops, there is an error!",
                                  description="Error report Nr. {} after reset.".format(self.counter),
                                  color=botcolor)
            embed.add_field(name='Server:', value='{}'.format(ctx.message.guild), inline=True)
            embed.add_field(name='Command:', value='{}'.format(ctx.message.content), inline=False)
            embed.add_field(name='Error:', value="```python\n{}```".format(error), inline=False)
            embed.add_field(name='Problems?',
                            value='Take a Picture of this message and contact us [here]({}).'.format(invite2),
                            inline=True)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text='Error Message', icon_url=ctx.message.author.avatar_url)
            embed.timestamp = datetime.utcnow()
            await ctx.channel.send(embed=embed)
            print(error)

    @commands.Cog.listener()
    async def on_ready(self):
        for server in self.bot.guilds:
            server_id = str(server.id)
            create_server(server_id)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            server_id = str(member.guild.id)
            user_id = str(member.id)
            create_user(server_id, user_id)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.bot:
            server_id = str(member.guild.id)
            user_id = str(member.id)
            # delete_user(server_id, user_id)

    #########################################################################################################################
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(692781491222085738)
        server_info1 = (datetime.now() - guild.created_at).days
        Bot = list(member.bot for member in guild.members if member.bot is True)
        user = list(member.bot for member in guild.members if member.bot is False)
        embed = discord.Embed(
            color=botcolor)
        embed.add_field(name='<:Neko_Logo:631245752722784283>__Server Join__<:Neko_Logo:631245752722784283>',
                        value='** **', inline=False)
        embed.add_field(name='Name:', value='{}'.format(guild.name), inline=True)
        embed.add_field(name='Server ID:', value='{}'.format(guild.id), inline=True)
        embed.add_field(name='Region:', value='{}'.format(guild.region), inline=True)
        embed.add_field(name='Membercount:', value='{} members'.format(guild.member_count), inline=True)
        embed.add_field(name='Botcount:', value='{} Bots'.format(str(len(Bot))), inline=True)
        embed.add_field(name='Humancount:', value='{} users'.format(str(len(user))), inline=True)
        embed.add_field(name='Large Server:', value='{} (250+ member)'.format(guild.large), inline=True)
        embed.add_field(name='Serverowner:', value='{}'.format(guild.owner), inline=True)
        embed.add_field(name='Verifylevel:', value='{} '.format(guild.verification_level), inline=True)
        embed.add_field(name='Created at:', value='{}'.format(
            "{} ({} days ago!)".format(guild.created_at.strftime("%d. %b. %Y %H:%M"), server_info1)), inline=False)
        embed.set_thumbnail(url="{0}".format(guild.icon_url))
        embed.set_footer(text='New Serverjoin', icon_url=guild.icon_url)
        embed.timestamp = datetime.utcnow()
        await channel.send(embed=embed)
        server_id = str(guild.id)
        create_server(server_id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(692781491222085738)
        embed = discord.Embed(title="", description="Marvin leaved *{0}*".format(guild.name),
                              color=discord.Color.blurple(),
                              timestamp=datetime.utcnow())
        embed.set_footer(text='This message was requested by Neko')
        await channel.send(embed=embed)
        server_id = str(guild.id)
        delete_server(server_id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            server_id = str(message.guild.id)
            user_id = str(message.author.id)
            DurationTillNextExp = request_setting(server_id, 'time_delay')
            CreditsPerMessage = request_setting(server_id, 'coins_per_message')
            MemberCredits = request_user_stats(server_id, user_id, 'money')
            MemberMessageCount = request_user_stats(server_id, user_id, 'message_count')
            LastMessageTime = request_user_stats(server_id, user_id, 'last_message_time')
            MessageSpeedDuration = round(time() - LastMessageTime)
            if MessageSpeedDuration > DurationTillNextExp:
                NewMessageCount = MemberMessageCount + 1
                NewCredits = MemberCredits + CreditsPerMessage
                edit_user_stats(server_id, user_id, 'last_message_time', time())
                edit_user_stats(server_id, user_id, 'message_count', NewMessageCount)
                edit_user_stats(server_id, user_id, 'money', NewCredits)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot:
            server_id = str(member.guild.id)
            user_id = str(member.id)
            try:
                if after.channel.type == before.channel.type and after.channel.type == discord.ChannelType.voice:
                    return
                elif after.channel.type == discord.ChannelType.voice:
                    set_join_time(server_id, user_id)
                elif before.channel.type == discord.ChannelType.voice:
                    ExpPerSecond = request_setting(server_id, 'coins_per_voice')
                    VoiceTime = request_user_stats(server_id, user_id, 'voice_time')
                    JoinTime = request_join_time(server_id, user_id)
                    ChannelDuration = round(time() - JoinTime)
                    VoiceExp = VoiceTime + ChannelDuration * ExpPerSecond
                    edit_user_stats(server_id, user_id, 'voice_time', VoiceExp)
                    delete_temp_user(server_id, user_id)
            except AttributeError:
                pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        server_id = str(channel.guild.id)
        if channel.type == discord.ChannelType.text:
            name = request_name_channel(server_id, str(channel.id))
            if name:
                delete_ticket(server_id, name, str(channel.id))
        if channel.type == discord.ChannelType.category:
            name = request_name_category(server_id, str(channel.id))
            if name:
                set_category(server_id, name, "0")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        server_id = str(message.guild.id)
        name = request_name_message(server_id, str(message.id))
        if name:
            set_message(server_id, name, "0")


def setup(bot):
    bot.add_cog(auto(bot))
