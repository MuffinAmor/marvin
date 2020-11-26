from discord.ext import commands
import asyncio
import random
import discord

bot = commands.Bot(command_prefix='m!')

botcolor = 0x000ffc

bot.remove_command('help')


class setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 800, commands.BucketType.channel)
    async def setup(self, ctx):
        def pred(m):
            return m.author == ctx.author and m.channel == ctx.channel
        await ctx.send("")
        while True:
            try:
                msg = await self.bot.wait_for('message', check=pred, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send('You took too long...')
                return
            if msg.content.lower() == "y":
                await ctx.send("Great!!!\nLet's start with few clarifications.")
                break
            elif msg.content.lower() == "n":
                await ctx.send("Oh, ok. see you next time than!")
                return
            else:
                await ctx.send("Ops, invalid input!\nType **y** for start and **n** for reject.")
                continue
        embed = discord.Embed(
            color=ctx.author.color)
        embed.set_author(name='Welcome in Marvins Ticket Setup')
        embed.add_field(name='Time:', value='You have 300 seconds for every Point before the next will starts.',
                        inline=False)
        embed.add_field(name='Skipping and Break up',
                        value='You can skip few points with **skip**\nWhen you will break up the Setup **end**',
                        inline=False)
        embed.set_thumbnail(
            url=self.bot.user.avatar_url)
        embed.set_footer(text='Do you need help? m!support')
        await ctx.send(embed=embed)
        await asyncio.sleep(20)
        await ctx.send("Heyo, glad to see u here! Let's Start with the Setup.")
        while True:
            try:
                msg = await self.bot.wait_for('message', check=pred, timeout=300.0)
            except asyncio.TimeoutError:
                await ctx.send('You took too long...\nLets go to the next question!')
                break
            if "skip" == msg.content:
                await ctx.send("Ok, lets skip this Question.")
                break
            elif "end" == msg.content:
                await ctx.send("Thats sad. I will delete your application. See you next time!")
                return
            else:
                age = msg.content
                await ctx.send("Alright you are **{}** years old.".format(age))
                break
        await ctx.send("───────────────────────────────────────────────────────────")
        await asyncio.sleep(3)
        await ctx.send("{}\nWhy do you apply? 2/7".format(random.choice(questions)))
        while True:
            try:
                msg = await self.bot.wait_for('message', check=pred, timeout=120.0)
            except asyncio.TimeoutError:
                await ctx.send('You took too long...\nLets go to the next question!')
                reason = "Outtimed"
                break
            if "skip" == msg.content:
                await ctx.send("Ok, lets skip this Question.")
                reason = "skipped"
                break
            elif "end" == msg.content:
                await ctx.send("Thats sad. I will delete your application. See you next time!")
                return
            else:
                reason = msg.content
                await ctx.send("{}\n{} ".format(random.choice(answers), reason))
                break
        await ctx.send("───────────────────────────────────────────────────────────")
        await asyncio.sleep(3)
        await ctx.send("{}\nFor which position do you apply? 3/7".format(random.choice(questions)))
        while True:
            try:
                msg = await self.bot.wait_for('message', check=pred, timeout=120.0)
            except asyncio.TimeoutError:
                await ctx.send('You took too long...\nLets go to the next question!')
                mod = "Outtimed"
                break
            if "skip" == msg.content:
                await ctx.send("Ok, lets skip this Question.")
                mod = "skipped"
                break
            elif "end" == msg.content:
                await ctx.send("Thats sad. I will delete your application. See you next time!")
                return
            else:
                mod = msg.content
                await ctx.send("{}\n{} ".format(random.choice(answers), mod))
                break
        await ctx.send("───────────────────────────────────────────────────────────")
        await asyncio.sleep(3)
        await ctx.send("{}\nWhats your skills? 4/7".format(random.choice(questions)))
        while True:
            try:
                msg = await self.bot.wait_for('message', check=pred, timeout=120.0)
            except asyncio.TimeoutError:
                await ctx.send('You took too long...\nLets go to the next question!')
                skills = "Outtimed"
                break
            if "skip" == msg.content:
                await ctx.send("Ok, lets skip this Question.")
                skills = "skipped"
                break
            elif "end" == msg.content:
                await ctx.send("Thats sad. I will delete your application. See you next time!")
                return
            else:
                skills = msg.content
                await ctx.send("You have amazing skills!\n{} ".format(skills))
                break
        await ctx.send("───────────────────────────────────────────────────────────")
        await asyncio.sleep(3)
        await ctx.send(
            "{}\nWhich languages do you can read and write except English? 5/7".format(random.choice(questions)))
        while True:
            try:
                msg = await self.bot.wait_for('message', check=pred, timeout=120.0)
            except asyncio.TimeoutError:
                await ctx.send('You took too long...\nLets go to the next question!')
                langs = "Outtimed"
                break
            if "skip" == msg.content:
                await ctx.send("Ok, lets skip this Question.")
                langs = "skipped"
                break
            elif "end" == msg.content:
                await ctx.send("Thats sad. I will delete your application. See you next time!")
                return
            else:
                langs = msg.content
                await ctx.send("{}\n{} ".format(random.choice(answers), langs))
                break
        await ctx.send("───────────────────────────────────────────────────────────")
        await asyncio.sleep(3)
        await ctx.send(
            "{} {}-chan.\nWhat do you do if someone offened you? 6/7".format(random.choice(questions), ctx.author.name))
        while True:
            try:
                msg = await self.bot.wait_for('message', check=pred, timeout=120.0)
            except asyncio.TimeoutError:
                await ctx.send('You took too long...\nLets go to the next question!')
                offended = "Outtimed"
                break
            if "skip" == msg.content:
                offended = "skipped"
                await ctx.send("Ok, lets skip this Question.")
                break
            elif "end" == msg.content:
                await ctx.send("Thats sad. I will delete your application. See you next time!")
                return
            else:
                offended = msg.content
                await ctx.send("{}\n{} ".format(random.choice(answers), offended))
                break
        await ctx.send("───────────────────────────────────────────────────────────")
        await asyncio.sleep(3)
        await ctx.send("{}\nDo you have any things that you would like add? 7/7".format(random.choice(questions)))
        while True:
            try:
                msg = await self.bot.wait_for('message', check=pred, timeout=120.0)
            except asyncio.TimeoutError:
                await ctx.send('You took too long...\nLets go to the end!')
                add = "Outtimed"
                break
            if "skip" == msg.content:
                await ctx.send("Ok, lets skip this Question.")
                add = "skipped"
                break
            elif "end" == msg.content:
                await ctx.send("Thats sad. I will delete your application. See you next time!")
                return
            else:
                add = msg.content
                await ctx.send("{}\n{} ".format(random.choice(answers), add))
                break
        await ctx.send(
            "Thank you very much for your application. I have send it to the Devs and will contact you if there is something new!")






def setup(bot):
    bot.add_cog(setup(bot))
