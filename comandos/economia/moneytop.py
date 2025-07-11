import discord
from discord.ext import commands
import json
import os

class MoneyTop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "economy.json"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.economy_data = json.load(f)
        else:
            self.economy_data = {}

    @commands.command(name='moneytop', aliases=['leaderboard', 'rank'])
    async def moneytop(self, ctx):
        # Pega os 20 maiores saldos
        users = [
            (int(uid), data.get("money", 0))
            for uid, data in self.economy_data.items()
        ]
        users.sort(key=lambda x: x[1], reverse=True)
        top_users = users[:20]

        desc = ""
        for idx, (user_id, money) in enumerate(top_users, 1):
            member = ctx.guild.get_member(user_id) or await self.bot.fetch_user(user_id)
            name = member.name if member else f"ID {user_id}"
            desc += f"**{idx}. {name}** - R$ {money:,}\n"

        embed = discord.Embed(
            title="🏆 Ranking dos Mais Ricos",
            description=desc or "Ninguém tem dinheiro ainda!",
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        await ctx.send(embed=embed, delete_after=10)

async def setup(bot):
    await bot.add_cog(MoneyTop(bot))
