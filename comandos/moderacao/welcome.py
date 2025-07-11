import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='welcome', help='Exibe instruções de configuração de entrada.')
    async def welcome(self, ctx):
        prefix = "'"  # Pode ser dinâmico se usar custom_prefix
        # Buscar canal e mensagem de entrada do banco, se implementado
        cnl = 'Não configurado'
        msg = 'Não configurado'
        embed = discord.Embed(
            title='Meow | Como configurar entrada',
            color=0x7289DA
        )
        embed.description = (
            f'Utilize `{prefix}entrada canal <#canal>`, para escolher um canal para enviar minha mensagem de entrada.\n'
            f'**Canal configurado para entrada: {cnl}**\n'
            f'Utilize `{prefix}entrada mensagem <mensagem>`, para escolher a mensagem que será enviada. *Use os parâmetros abaixo!*\n'
            f'**Mensagem de entrada:** `{msg}`\n'
            f'Utilize `{prefix}entrada reset canal` ou `{prefix}entrada reset mensagem` para resetar.'
        )
        embed.add_field(
            name='Parâmetros',
            value='```{user} = Menciona o usuário\n{guild} = Mostra o nome do servidor\n{count} = Quantidade de membros no servidor\n{id} = Mostra o id do Usuário```'
        )
        embed.set_footer(text=f'Autor do comando: {ctx.author}')
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
          
