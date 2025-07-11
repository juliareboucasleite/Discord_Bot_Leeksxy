import discord
from discord.ext import commands

class ServerIcon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='servericon', help='Exibe o ícone do servidor em um embed.')
    async def servericon(self, ctx):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        guild = ctx.guild
        icon_url = guild.icon.url if guild.icon else None
        if not icon_url:
            await ctx.send('Este servidor não possui um ícone definido.')
            return
        embed = discord.Embed(
            title=f'Ícone do servidor {guild.name}',
            description=f'[Clique aqui para baixar a imagem.]({icon_url})',
            color=discord.Color.random()
        )
        embed.set_image(url=icon_url)
        embed.set_footer(text=f'Solicitado por {ctx.author}', icon_url=ctx.author.display_avatar.url)
        msg = await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ServerIcon(bot))