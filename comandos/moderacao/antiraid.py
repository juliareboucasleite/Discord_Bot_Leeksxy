import discord
from discord.ext import commands
from typing import Optional

ROLE_ID = 768838536538751006  # ID do cargo autorizado

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='antiraid')
    @commands.has_permissions(administrator=True)
    async def antiraid(self, ctx, modo: Optional[str] = None):
        roleA = ctx.guild.get_role(ROLE_ID)
        if not roleA:
            return await ctx.send(f"Cargo alvo não encontrado (ID: {ROLE_ID})!")

        if not any(r.id == ROLE_ID for r in ctx.author.roles):
            return await ctx.send(f"{ctx.author.mention} esse comando é restrito ao cargo específico.")

        if modo not in ['on', 'off']:
            return await ctx.send(f"{ctx.author.mention} a sintaxe correta é `'antiraid on'` ou `'antiraid off'`.")

        try:
            await roleA.edit(permissions=discord.Permissions.none(), reason=f"Antiraid {modo} por {ctx.author}")
        except Exception as e:
            return await ctx.send(f"Erro ao alterar permissões do cargo: {e}")

        cor = 0x43B581 if modo == 'on' else 0xFF0000
        embed = discord.Embed(
            title=f"🛡️ Sistema de Antiraid {'Ativado' if modo == 'on' else 'Desativado'}",
            description=f"O sistema de Antiraid foi {'ligado' if modo == 'on' else 'desligado'} por {ctx.author.mention}",
            color=cor
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AntiRaid(bot))