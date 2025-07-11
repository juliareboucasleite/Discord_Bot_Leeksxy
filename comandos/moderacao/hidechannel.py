import discord
from discord.ext import commands

class HideChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hidechannel', aliases=['esconderchat', 'esconderCanal', 'escondercanal'], help='Deixa o canal invisível para @everyone.')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def hidechannel(self, ctx):
        role = ctx.guild.default_role  # @everyone
        try:
            await ctx.channel.set_permissions(role, view_channel=False)
            await ctx.send('Canal invisível com sucesso!!\nUse `viewchannel` para deixar visível.')
        except discord.Forbidden:
            await ctx.send('Permissões insuficientes para alterar a visibilidade do canal.')
        except Exception as e:
            await ctx.send(f'Erro ao alterar a visibilidade do canal: {e}')

async def setup(bot):
    await bot.add_cog(HideChannel(bot))