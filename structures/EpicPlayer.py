import discord
from discord.ext import commands
from structures.Logger import Logger

class EpicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger("Logs.log")
        self.commands_ran = 0
        self.songs_played = 0

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.log("EpicPlayer pronto!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")
        self.commands_ran += 1
        self.logger.log(f"Comando ping executado por {ctx.author}")

# Para carregar este cog, use: bot.load_extension('structures.EpicPlayer')

def setup(bot):
    bot.add_cog(EpicPlayer(bot))
