import discord
from discord.ext import commands
import webcolors
from typing import Optional

class CreateRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='createrole', help='Cria um novo cargo no servidor. Uso: createrole <cor> <nome>')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def createrole(self, ctx, color: Optional[str] = None, *, name: Optional[str] = None):
        if not color or not name:
            return await ctx.send('Uso correto: `createrole <cor> <nome>`')
        if not name.isalnum():
            return await ctx.send('O nome do cargo só pode conter letras e números.')
        if len(name) > 100:
            return await ctx.send('O nome do cargo não pode ter mais de 100 caracteres.')
        try:
            hex_color = webcolors.name_to_hex(color.lower())
            color_value = int(hex_color.lstrip('#'), 16)
        except Exception:
            return await ctx.send('Cor inválida. Use um nome de cor em inglês, ex: `red`, `blue`, `green`.')
        try:
            role = await ctx.guild.create_role(name=name, color=discord.Color(color_value), reason=f'Criado por {ctx.author}')
        except discord.Forbidden:
            return await ctx.send('Permissões insuficientes para criar o cargo.')
        except Exception as e:
            return await ctx.send(f'Erro ao criar o cargo: {e}')
        embed = discord.Embed(
            title='Novo Cargo Criado',
            description=f'**Cargo:** {role.mention}\n**Cor:** {color}\n**Criado por:** {ctx.author.mention}',
            color=color_value
        )
        embed.set_author(name=f'{ctx.author} - ({ctx.author.id})', icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CreateRole(bot))