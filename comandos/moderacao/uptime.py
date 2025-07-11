
import discord
from discord.ext import commands
from datetime import datetime

class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='uptime')
    async def uptime(self, ctx):
        """Mostra há quanto tempo o bot está online"""
        
        # Calculate uptime
        total_seconds = int(self.bot.uptime.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        embed = discord.Embed(
            title="⏰ Uptime",
            description=f"Estou online há: **{days}d {hours}h {minutes}m {seconds}s**",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Uptime(bot))
