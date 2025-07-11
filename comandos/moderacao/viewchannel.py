import discord
from discord.ext import commands

class ViewChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='viewchannel', aliases=['viewChannel', 'mostrarCanal', 'mostrarcanal'], help='Deixa o canal visível para @everyone.')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def viewchannel(self, ctx):
        role = ctx.guild.default_role  # @everyone
        try:
            await ctx.channel.set_permissions(role, view_channel=True)
            await ctx.send('Canal visível com sucesso!!\nUse `hidechannel` para deixar invisível.')
        except discord.Forbidden:
            await ctx.send('Permissões insuficientes para alterar a visibilidade do canal.')
        except Exception as e:
            await ctx.send(f'Erro ao alterar a visibilidade do canal: {e}')

async def setup(bot):
    await bot.add_cog(ViewChannel(bot))