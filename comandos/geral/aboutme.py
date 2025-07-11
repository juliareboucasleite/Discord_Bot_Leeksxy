import discord
from discord.ext import commands
import json
import os

class AboutMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = "data/aboutme.json"
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

    @commands.command(name="aboutme", aliases=["about", "sobremim"])
    async def aboutme(self, ctx, *, texto=None):
        if not texto:
            return await ctx.send("✏️ Digite depois do comando o seu **About Me**.")
        if len(texto) > 500:
            return await ctx.send("⚠️ Faça um About Me com menos de 500 caracteres.")

        self.data[str(ctx.author.id)] = texto
        self._save()

        embed = discord.Embed(
            title="📘 About Me",
            description=f"Seu About Me foi salvo como:\n\n**{texto}**\n\nUse `'perfil` para ver!",
            color=discord.Color.random()
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AboutMe(bot))
