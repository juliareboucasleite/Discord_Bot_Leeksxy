import discord
from discord.ext import commands

class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lock', help='Bloqueia o canal para @everyone (impede o envio de mensagens).')
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lock(self, ctx):
        role = ctx.guild.default_role  # @everyone
        try:
            await ctx.message.delete()
        except Exception:
            pass
        try:
            await ctx.channel.set_permissions(role, send_messages=False)
            embed = discord.Embed(
                title='🔒 Canal Bloqueado',
                description='Este canal foi bloqueado para o envio de mensagens por @everyone.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send('Permissões insuficientes para bloquear o canal.')
        except Exception as e:
            await ctx.send(f'Erro ao bloquear o canal: {e}')

def setup(bot):
    bot.add_cog(Lock(bot))