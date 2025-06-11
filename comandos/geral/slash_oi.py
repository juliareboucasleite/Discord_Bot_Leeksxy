import discord
from discord import app_commands
from discord.ext import commands

class SlashExemplo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="oi", description="O bot diz oi!")
    async def slash_oi(self, interaction: discord.Interaction):
        await interaction.response.send_message("👋 Oi! Eu sou um bot com comando de barra!")

async def setup(bot):
    await bot.add_cog(SlashExemplo(bot))
