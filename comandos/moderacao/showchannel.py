import discord
from discord.ext import commands

class ShowChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='showchannel', help='Torna o canal visível para @everyone.')
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def showchannel(self, ctx):
        role = ctx.guild.default_role  # @everyone
        try:
            await ctx.channel.set_permissions(role, view_channel=True)
            await ctx.send('Canal apareceu!')
        except discord.Forbidden:
            await ctx.send('Permissões insuficientes para mostrar o canal.')
        except Exception as e:
            await ctx.send(f'Erro ao mostrar o canal: {e}')

async def setup(bot):
    await bot.add_cog(ShowChannel(bot))