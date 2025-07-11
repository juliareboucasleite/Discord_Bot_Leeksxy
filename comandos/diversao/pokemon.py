import discord
from discord.ext import commands
import aiohttp

class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pokemon")
    async def pokemon(self, ctx, *, nome=None):
        if not nome:
            await ctx.send("Por favor, diga o nome de um Pokémon!")
            return

        url = f"https://courses.cs.washington.edu/courses/cse154/webservices/pokedex/pokedex.php?pokemon={nome}"

        msg = await ctx.send("🔍 Buscando informações da API...")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await msg.edit(content="❌ Pokémon não encontrado ou erro na API.")
                    return
                body = await resp.json()

        embed = discord.Embed(
            description=body["info"]["description"],
            color=discord.Color.red()
        )
        embed.set_author(
            name=body["name"],
            icon_url=f"https://courses.cs.washington.edu/courses/cse154/webservices/pokedex/{body['images']['typeIcon']}"
        )
        embed.set_thumbnail(
            url=f"https://courses.cs.washington.edu/courses/cse154/webservices/pokedex/{body['images']['photo']}"
        )
        embed.set_footer(
            text=f"Fraqueza do Pokémon - {body['info']['weakness']}",
            icon_url=f"https://courses.cs.washington.edu/courses/cse154/webservices/pokedex/{body['images']['weaknessIcon']}"
        )

        await ctx.send(embed=embed)
        await msg.delete()

def setup(bot):
    bot.add_cog(Pokemon(bot))
