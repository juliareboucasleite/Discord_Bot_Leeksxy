import discord
from discord.ext import commands
from typing import Optional

class Trash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="trash", aliases=["lixo"])
    async def trash(self, ctx, member: Optional[discord.Member] = None):
        if not member:
            return await ctx.send("🗑️ Fale alguém para jogar no lixo.")
        if ctx.author.id == member.id:
            return await ctx.send("🗑️ Você não pode jogar a si mesmo no lixo.")

        face = ctx.author.display_avatar.url
        trash = member.display_avatar.url

        # Construção da URL da API com parâmetros
        image_url = f"https://api.alexflipnote.dev/trash?face={face}&trash={trash}"

        embed = discord.Embed(
            title="A lixeira é sua casa 🗑️",
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Trash(bot))
