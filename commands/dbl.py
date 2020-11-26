import dbl
from discord.ext import commands


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYzOTk1NTY5MDgzNTgwNDE3MCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTg4NjE1MDExfQ.j-7QGhPqQlwgwRbDyOpoM96HGcZ2wYlIPXQHltB17c8'  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token,
                                   autopost=True)  # Autopost will post your guild count every 30 minutes

    async def on_guild_post(self):
        print("Server count posted successfully")


def setup(bot):
    bot.add_cog(TopGG(bot))
