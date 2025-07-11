import discord
from discord.ext import commands
import json
import os
import random
import time
from datetime import datetime
from typing import Optional

class Roubar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balances_file = "data/balances.json"
        self.cooldown_file = "data/roubo_cooldown.json"
        self._load()

    def _load(self):
        if not os.path.exists(self.balances_file):
            with open(self.balances_file, "w") as f:
                json.dump({}, f)
        if not os.path.exists(self.cooldown_file):
            with open(self.cooldown_file, "w") as f:
                json.dump({}, f)
        with open(self.balances_file, "r") as f:
            self.balances = json.load(f)
        with open(self.cooldown_file, "r") as f:
            self.cooldowns = json.load(f)

    def _save(self):
        with open(self.balances_file, "w") as f:
            json.dump(self.balances, f, indent=4)
        with open(self.cooldown_file, "w") as f:
            json.dump(self.cooldowns, f, indent=4)

    def get_money(self, uid):
        return self.balances.get(str(uid), {}).get("money", 0)

    def set_money(self, uid, valor):
        uid = str(uid)
        if uid not in self.balances:
            self.balances[uid] = {"money": 0, "bank": 0}
        self.balances[uid]["money"] = max(0, valor)

    @commands.command(name="roubar", aliases=["rob", "roubo"])
    async def roubar(self, ctx, membro: Optional[discord.Member] = None):
        autor = ctx.author
        if not membro:
            return await ctx.send("🍪 | Você precisa mencionar alguém para roubar!")
        if membro.id == autor.id:
            return await ctx.send("🍪 | Você não pode se auto-roubar!")
        saldo_alvo = self.get_money(membro.id)
        saldo_autor = self.get_money(autor.id)
        if saldo_alvo <= 0:
            return await ctx.send("🍪 | Você não pode roubar alguém que não tem cookies!")
        cooldown = 86400  # 24h
        agora = int(time.time())
        ultimo_roubo = self.cooldowns.get(str(autor.id), 0)
        restante = cooldown - (agora - ultimo_roubo)
        if restante > 0:
            h = restante // 3600
            m = (restante % 3600) // 60
            s = restante % 60
            embed = discord.Embed(
                description=f"Você já realizou um roubo hoje!\nTente novamente em **{h}h {m}m {s}s**",
                color=discord.Color.dark_gray()
            )
            return await ctx.send(embed=embed)
        azar = random.randint(1, 4)
        if azar == 2 and saldo_autor > 0:
            perda = random.randint(1, saldo_autor)
            self.set_money(autor.id, saldo_autor - perda)
            self.cooldowns[str(autor.id)] = agora
            self._save()
            embed = discord.Embed(
                title="⚠️ Prejuízo por Roubo",
                description=f"Você tentou roubar um forno... e perdeu **{perda} cookies**!",
                color=discord.Color.dark_gray()
            )
            return await ctx.send(embed=embed)
        ganho = random.randint(1, saldo_alvo)
        self.set_money(autor.id, saldo_autor + ganho)
        self.set_money(membro.id, saldo_alvo - ganho)
        self.cooldowns[str(autor.id)] = agora
        self._save()
        embed = discord.Embed(
            title="💰 Roubo Realizado",
            description=f"Você roubou {membro.mention} e ganhou **{ganho} cookies**!",
            color=discord.Color.green()
        )
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Roubar(bot))
