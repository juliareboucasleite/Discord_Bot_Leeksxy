import discord
from discord.ext import commands

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='unlock', help='Desbloqueia o canal para @everyone (visualizar e enviar mensagens).')
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        role = ctx.guild.default_role  # @everyone
        try:
            await ctx.channel.set_permissions(role, view_channel=True, send_messages=True)
            await ctx.send('Canal desbloqueado!')
        except discord.Forbidden:
            await ctx.send('Permissões insuficientes para desbloquear o canal.')
        except Exception as e:
            await ctx.send(f'Erro ao desbloquear o canal: {e}')

async def setup(bot):
    await bot.add_cog(Unlock(bot))