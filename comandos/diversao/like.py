import discord
from discord.ext import commands
import json
import os
import time

class Like(commands.Cog):
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

    @commands.command(name="like", aliases=["likes"])
    async def like(self, ctx):
        if not ctx.message.mentions:
            await ctx.send("Por favor fale alguém para dar um like!!")
            return
        member = ctx.message.mentions[0]
        if member.id == ctx.author.id:
            await ctx.send("Você não pode dar like em si mesmo!")
            return
        author_id = str(ctx.author.id)
        member_id = str(member.id)
        timeout = 4300  # em segundos (1h11min)
        current_time = int(time.time())
        last_like_time = self.cooldown.get(author_id, 0)
        remaining = timeout - (current_time - last_like_time)
        if remaining > 0:
            h = remaining // 3600
            m = (remaining % 3600) // 60
            s = remaining % 60
            return await ctx.reply(f":alarm_clock: Você já deu um like hoje. Tente novamente em {h}h {m}m {s}s")
        msg = await ctx.send(f"Você está dando um like para {member.mention}! Para confirmar, clique em 👍")
        await msg.add_reaction("👍")
        def check(reaction, user):
            return (
                user.id == ctx.author.id
                and str(reaction.emoji) == "👍"
                and reaction.message.id == msg.id
            )
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
        except:
            await ctx.send("⏰ Tempo esgotado para confirmar.")
            return
        await msg.delete()
        self.rep[member_id] = self.rep.get(member_id, 0) + 1
        self.cooldown[author_id] = current_time
        self._save()
        await ctx.send(":+1: Seu like foi entregue com sucesso!")

def setup(bot):
    bot.add_cog(Like(bot))
