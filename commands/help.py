from datetime import datetime

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.')

botcolor = 0x00ff06

bot.remove_command('help')

url = 'https://cdn.discordapp.com/attachments/522437022095245313/546359964101509151/Neko_Logo.png'


class HelpClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command(pass_context=True)
    async def help(self, ctx):
        if ctx.author.bot == False:
            embed = discord.Embed(
                color=ctx.author.color)
            embed.set_author(name='Hilfe und Anderes')
            embed.add_field(name='❓', value='General Commands.', inline=False)
            embed.add_field(name='📁', value='Ticket System Commands.', inline=False)
            embed.add_field(name='🏢', value='Shop System Commands.', inline=False)
            embed.add_field(name='🔙', value='Go back to this site', inline=False)
            embed.set_thumbnail(url=url)
            embed.set_footer(text='Do you need help? m!support')
            embed.timestamp = datetime.utcnow()
            msg = await ctx.channel.send(embed=embed)
            await msg.add_reaction("❓")
            await msg.add_reaction("📁")
            await msg.add_reaction("🏢")
            await msg.add_reaction("🔙")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.author.id == self.bot.user.id:
            if not user.bot:
                if reaction.emoji == "❓":
                    embed = discord.Embed(
                        color=user.color)
                    embed.set_author(name='General Commands.')
                    embed.add_field(name="m!support", value="Gives you a link to our Supportserver", inline=False)
                    embed.add_field(name="m!invite", value="Gives you a link to invite Marvin", inline=False)
                    embed.add_field(name='m!balance',
                                    value='How much Coins do you have?',
                                    inline=False)
                    embed.add_field(name='m!shop',
                                    value='Open the Role Shop!',
                                    inline=False)
                    embed.add_field(name='m!buy *token*',
                                    value='Buy a Role from the Shop.',
                                    inline=False)
                    embed.add_field(name='m!settings',
                                    value='Shows you the Server Settings.',
                                    inline=False)
                    embed.add_field(name='**🔙**', value='Go back to navigation site', inline=False)
                    embed.set_thumbnail(
                        url=url)
                    embed.set_footer(text='Do you need help? m!support')
                    await reaction.message.edit(embed=embed)
                    await reaction.message.remove_reaction("❓", user)
                if reaction.emoji == "📁":
                    embed = discord.Embed(
                        color=user.color)
                    embed.set_author(name='Ticket System Commands.')
                    embed.add_field(name='**m!ticketgroups**',
                                    value='Show your Ticket Groups!',
                                    inline=False)
                    embed.add_field(name='**m!create_ticket_group *name***',
                                    value='Create a Ticket Group!',
                                    inline=False)
                    embed.add_field(name='**m!delete_ticket_group *name***',
                                    value='Delete a Ticket Group!',
                                    inline=False)
                    embed.add_field(name='**m!set_log *channel* *ticketgroup***',
                                    value='Set the Ticket Log.!',
                                    inline=False)
                    embed.add_field(name='**m!set_category *category* *ticketgroup***',
                                    value='Set the Ticket Category!',
                                    inline=False)
                    embed.add_field(name='**m!activ_ticket *ticketgroup***',
                                    value='Activate the Ticket Group!',
                                    inline=False)
                    embed.timestamp = datetime.utcnow()
                    embed.add_field(name='🔙', value='Go back to navigation site', inline=False)
                    embed.set_thumbnail(url=url)
                    embed.set_footer(text='Do you need help? m!support')
                    await reaction.message.edit(embed=embed)
                    await reaction.message.remove_reaction("📁", user)
                if reaction.emoji == "🏢":
                    embed = discord.Embed(
                        color=user.color)
                    embed.set_author(name='Shop System Commands.')
                    embed.add_field(name='m!add_role *role* *coins*',
                                    value='Add a Role to the Shop.',
                                    inline=False)
                    embed.add_field(name='m!remove_role *key*',
                                    value='Remove a Role from the Shop.',
                                    inline=False)
                    embed.add_field(name='m!set_delay *time*',
                                    value='Set the Spam delay for the coin gathering.',
                                    inline=False)
                    embed.add_field(name='m!set_msg_coins *coins*',
                                    value='Set the Coins that you can gather per Message',
                                    inline=False)
                    embed.add_field(name='set_voice_coins *coins*',
                                    value='Set the Coins per Minute in the Voice Chat.',
                                    inline=False)
                    embed.timestamp = datetime.utcnow()
                    embed.add_field(name='🔙', value='Go back to navigation site', inline=False)
                    embed.set_thumbnail(url=url)
                    embed.set_footer(text='Do you need help? m!support')
                    await reaction.message.edit(embed=embed)
                    await reaction.message.remove_reaction("🏢", user)
                if reaction.emoji == "🔙":
                    embed = discord.Embed(
                        color=user.color)
                    embed.set_author(name='Hilfe und Anderes')
                    embed.add_field(name='❓', value='General Commands.', inline=False)
                    embed.add_field(name='📁', value='Ticket System Commands.', inline=False)
                    embed.add_field(name='🏢', value='Shop System Commands.', inline=False)
                    embed.add_field(name='🔙', value='Go back to this site', inline=False)
                    embed.set_thumbnail(
                        url=url)
                    embed.set_footer(text='Do you need help? m!support')
                    embed.timestamp = datetime.utcnow()
                    await reaction.message.edit(embed=embed)
                    await reaction.message.remove_reaction("🔙", user)


def setup(bot):
    bot.add_cog(HelpClass(bot))
