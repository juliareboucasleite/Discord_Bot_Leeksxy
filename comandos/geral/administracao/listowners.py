import discord
from discord.ext import commands
import os

OWNER_IDS = os.getenv("CRIADORA_ID", "").split(",")

class ListOwners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="listowners", help="Lista os donos atuais do bot (OWNER_IDS do .env)")
    async def listowners(self, ctx):
        mentions = []
        for oid in OWNER_IDS:
            oid = oid.strip()
            if oid.isdigit():
                user = self.bot.get_user(int(oid))
                if user:
                    mentions.append(f"{user.mention} ({oid})")
                else:
                    mentions.append(f"<@{oid}> ({oid})")
        if not mentions:
            await ctx.send("Nenhum dono configurado no .env!")
            return
        embed = discord.Embed(
            title="👑 Donos do Bot",
            description="\n".join(mentions),
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ListOwners(bot)) 