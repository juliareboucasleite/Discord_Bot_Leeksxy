
import discord
from discord.ext import commands
import json
import os
from typing import Optional

class Balance(commands.Cog):
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

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.economy_data, f, indent=2)

    def get_user_balance(self, user_id):
        user_id = str(user_id)
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {"money": 0, "bank": 0}
            self.save_data()
        return self.economy_data[user_id]

    @commands.command(name='balance', aliases=['bal', 'saldo'])
    async def balance(self, ctx, member: Optional[discord.Member] = None):
        """Mostra o saldo de alguém"""
        if member is None:
            member = ctx.author
        assert member is not None  # Garante para o linter que member nunca será None
        user_data = self.get_user_balance(member.id)
        
        embed = discord.Embed(
            title=f"💰 Carteira de {member.display_name}",
            color=0x00ff00
        )
        embed.add_field(name="Dinheiro", value=f"R$ {user_data['money']:,}", inline=True)
        embed.add_field(name="Banco", value=f"R$ {user_data['bank']:,}", inline=True)
        embed.add_field(name="Total", value=f"R$ {user_data['money'] + user_data['bank']:,}", inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Balance(bot))
