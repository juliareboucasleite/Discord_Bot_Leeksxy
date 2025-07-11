import discord
from discord.ext import commands
import json
import os
from typing import Optional

class VerReputacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = "data/reputacao.json"
        self._load()

    def _load(self):
        if not os.path.exists(self.file):
            os.makedirs(os.path.dirname(self.file), exist_ok=True)
            with open(self.file, "w") as f:
                json.dump({"rep": {}}, f)
        with open(self.file, "r") as f:
            self.data = json.load(f)

    @commands.command(name="reputacao", aliases=["rep"])
    async def reputacao(self, ctx, member: Optional[discord.Member] = None):
        member = member or ctx.author
        rep = self.data["rep"].get(str(member.id), 0)

        embed = discord.Embed(
            title="📈 Reputação",
            description=f"{member.mention} tem **{rep} ponto(s)** de reputação.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(VerReputacao(bot))
