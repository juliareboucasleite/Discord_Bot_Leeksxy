import discord
from discord.ext import commands
import json
import os

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = "data/prefixes.json"
        self.default_prefix = "'"
        self._load()

    def _load(self):
        if not os.path.exists(self.file):
            os.makedirs(os.path.dirname(self.file), exist_ok=True)
            with open(self.file, "w") as f:
                json.dump({}, f)
        with open(self.file, "r") as f:
            self.prefixes = json.load(f)

    def _save(self):
        with open(self.file, "w") as f:
            json.dump(self.prefixes, f, indent=4)

    @commands.command(name="prefix", aliases=["prefixo", "prfx", "prefix2"])
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix=None):
        gid = str(ctx.guild.id)

        if not new_prefix:
            return await ctx.send("⚠️ Fale um prefixo com até 3 caracteres!")

        if len(new_prefix) > 3:
            return await ctx.send("❌ Prefixo muito longo! Use até 3 caracteres.")

        if new_prefix == self.default_prefix:
            self.prefixes.pop(gid, None)
            self._save()
            return await ctx.send("✅ Prefixo voltou a ser o padrão `'`")

        self.prefixes[gid] = new_prefix
        self._save()
        await ctx.send(f"✅ Prefixo atualizado para `{new_prefix}`")

def setup(bot):
    bot.add_cog(Prefix(bot))
