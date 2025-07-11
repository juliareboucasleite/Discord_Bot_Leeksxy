import discord
from discord.ext import commands

class Recrutadores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='recrutadores', help='Mostra o ranking dos 5 maiores recrutadores do servidor (convites).')
    @commands.has_permissions(manage_guild=True)
    async def recrutadores(self, ctx):
        try:
            invites = await ctx.guild.invites()
        except discord.Forbidden:
            await ctx.send('Não tenho permissão para ver os convites deste servidor.')
            return
        except Exception as e:
            await ctx.send(f'Ocorreu um erro ao buscar os convites: {e}')
            return
        if not invites:
            await ctx.send('Este servidor não possui convites!')
            return
        # Ordena por número de usos
        rank = sorted(invites, key=lambda i: i.uses, reverse=True)[:5]
        if len(rank) < 5:
            await ctx.send('Este servidor precisa possuir pelo menos 5 convites para ter um ranking.')
            return
        total = sum(i.uses for i in rank)
        embed = discord.Embed(
            title=f'Recrutadores | {ctx.guild.name}',
            description='Esse é meu ranking e apenas os melhores no recrutamento se encontram nele!',
            color=discord.Color.random()
        )
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        for idx, invite in enumerate(rank, 1):
            user = invite.inviter
            embed.add_field(
                name=f'**{idx}º** {user}',
                value=f'`Convidados: {invite.uses}`',
                inline=False
            )
        embed.add_field(name='Total/Recrutados', value=f'{total}', inline=True)
        embed.add_field(name='Total/Convites', value=f'{len(invites)}', inline=True)
        embed.set_footer(text=f'Requisitado por {ctx.author} - ID {ctx.author.id}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Recrutadores(bot))
