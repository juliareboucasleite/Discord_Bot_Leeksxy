import discord
from discord.ext import commands
import json
import os
import time

class DarReputacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rep_file = "data/reputacao.json"
        self.cooldown_file = "data/rep_cooldown.json"
        self._load()

    def _load(self):
        if not os.path.exists(self.rep_file):
            with open(self.rep_file, "w") as f:
                json.dump({}, f)
        if not os.path.exists(self.cooldown_file):
            with open(self.cooldown_file, "w") as f:
                json.dump({}, f)
        with open(self.rep_file, "r") as f:
            self.rep = json.load(f)
        with open(self.cooldown_file, "r") as f:
            self.cooldown = json.load(f)

    def _save(self):
        with open(self.rep_file, "w") as f:
            json.dump(self.rep, f, indent=4)
        with open(self.cooldown_file, "w") as f:
            json.dump(self.cooldown, f, indent=4)

    @commands.command(name="darrep", aliases=["like", "likes"])
    async def darrep(self, ctx):
        if not ctx.message.mentions:
            return await ctx.send("Por favor, mencione alguém para dar reputação!")
        alvo = ctx.message.mentions[0]
        if alvo.id == ctx.author.id:
            return await ctx.send("Você não pode dar reputação a si mesmo!")
        author_id = str(ctx.author.id)
        alvo_id = str(alvo.id)
        cooldown_time = 3600 * 1 + 300  # 1h e 5 min
        agora = int(time.time())
        ultimo = self.cooldown.get(author_id, 0)
        if cooldown_time - (agora - ultimo) > 0:
            restante = cooldown_time - (agora - ultimo)
            h = restante // 3600
            m = (restante % 3600) // 60
            s = restante % 60
            return await ctx.reply(f"⏳ Você já deu reputação recentemente. Tente novamente em {h}h {m}m {s}s.")
        msg = await ctx.send(f"{ctx.author.mention}, confirme sua reputação para {alvo.mention} clicando em 👍")
        await msg.add_reaction("👍")
        def check(reaction, user):
            return (
                user.id == ctx.author.id and str(reaction.emoji) == "👍" and reaction.message.id == msg.id
            )
        try:
            await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
        except:
            return await ctx.send("⏰ Tempo esgotado para confirmar.")
        await msg.delete()
        self.rep[alvo_id] = self.rep.get(alvo_id, 0) + 1
        self.cooldown[author_id] = agora
        self._save()
        await ctx.send(f"👍 Reputação entregue a {alvo.mention} com sucesso!")

def setup(bot):
    bot.add_cog(DarReputacao(bot))
