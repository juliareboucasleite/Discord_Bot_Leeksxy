import discord
from discord.ext import commands
from typing import Optional

REPORT_CHANNEL_ID = 707653323695718522  # ID do canal de reports

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='report', help='Reporta um usuário para a staff. Uso: report <@usuário> <motivo>')
    async def report(self, ctx, member: Optional[discord.Member] = None, *, motivo: Optional[str] = None):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        if not member:
            return await ctx.send('Mencione quem você quer reportar!')
        if not motivo:
            return await ctx.send('Especifique um motivo! Não é possível reportar alguém sem um motivo.')
        embed = discord.Embed(
            title='Usuário reportado.',
            color=0xfbff00
        )
        embed.set_thumbnail(url='https://www.pinclipart.com/picdir/middle/1-12435_ace-attorney-clipart-objection-ace-attorney-objection-meme.png')
        embed.add_field(name='Usuário reportado:', value=f'{member} (ID: {member.id})', inline=False)
        embed.add_field(name='Reportado por:', value=f'{ctx.author} (ID: {ctx.author.id})', inline=False)
        embed.add_field(name='Hora:', value=ctx.message.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=False)
        embed.add_field(name='Motivo:', value=motivo, inline=False)
        report_channel = ctx.guild.get_channel(REPORT_CHANNEL_ID)
        if not report_channel:
            return await ctx.send('Canal de reports não encontrado. Avise a staff.')
        await report_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Report(bot))