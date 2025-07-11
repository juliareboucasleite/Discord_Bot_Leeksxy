import discord
from discord.ext import commands
import json
import os
from typing import Optional

OWNER_IDS = os.getenv("CRIADORA_ID", "").split(",")

class AddMoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = "data/reputacao.json"
        self._load()

    def _load(self):
        if not os.path.exists(self.file):
            os.makedirs(os.path.dirname(self.file), exist_ok=True)
            with open(self.file, "w") as f:
                json.dump({}, f)
        with open(self.file, "r") as f:
            self.data = json.load(f)

    def _save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    @commands.command(name="addmoney", aliases=["addrep"])
    async def addmoney(self, ctx, member: Optional[discord.Member] = None, valor: Optional[int] = None):
        if str(ctx.author.id) not in OWNER_IDS:
            return await ctx.send("❌ Apenas meu criador pode usar esse comando!")

        if not member:
            return await ctx.send("👤 Você precisa mencionar alguém!")

        if valor is None:
            return await ctx.send("💰 Especifique quanto você quer adicionar.")

        if not isinstance(valor, int):
            return await ctx.send("❌ O valor precisa ser um número inteiro.")

        msg = await ctx.send(
            f"⚠️ Você quer realmente adicionar **{valor}** pontos de reputação para {member.mention}?"
        )
        await msg.add_reaction("👍")

        def check(reaction, user):
            return (
                user.id == ctx.author.id and str(reaction.emoji) == "👍" and reaction.message.id == msg.id
            )

        try:
            await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
        except:
            return await ctx.send("⏰ Tempo esgotado. Cancelado.")

        self.data[str(member.id)] = self.data.get(str(member.id), 0) + valor
        self._save()
        await ctx.send(f"✅ Reputação adicionada com sucesso para {member.mention}!")

def setup(bot):
    bot.add_cog(AddMoney(bot))
