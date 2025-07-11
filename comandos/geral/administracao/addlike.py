import discord
from discord.ext import commands
import json
import os
from typing import Optional

OWNER_IDS = os.getenv("CRIADORA_ID", "").split(",")

class AddLike(commands.Cog):
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

    @commands.command(name="addlike", aliases=["addlikes"])
    async def addlike(self, ctx, quantia: Optional[int] = None, membro: Optional[discord.Member] = None):
        if str(ctx.author.id) not in OWNER_IDS:
            return await ctx.send("🔒 Apenas meu desenvolvedor pode usar esse comando.")

        if quantia is None or quantia <= 0:
            return await ctx.send("❌ Escreva uma quantia válida (maior que 0) para adicionar.")

        membro = membro or ctx.author
        uid = str(membro.id)

        self.data[uid] = self.data.get(uid, 0) + quantia
        self._save()

        await ctx.send(
            f"👍 {ctx.author.display_name} adicionou **{quantia}** likes à conta de **{membro.display_name}**!"
        )

def setup(bot):
    bot.add_cog(AddLike(bot))
