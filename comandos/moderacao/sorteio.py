import discord
from discord.ext import commands
import asyncio
import re
from typing import Optional

class Sorteio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sorteio', help='Cria um sorteio simples. Uso: sorteio <tempo> <#canal> <prêmio>')
    @commands.has_permissions(administrator=True)
    async def sorteio(self, ctx, tempo: Optional[str] = None, canal: Optional[discord.TextChannel] = None, *, premio: Optional[str] = None):
        if not tempo:
            return await ctx.send('Você não especificou seu tempo!')
        match = re.match(r'^(\d+)([mhd])$', tempo)
        if not match:
            return await ctx.send('Você não usou a formatação correta para a hora! Exemplo: 10m, 1h, 2d')
        tempo_num = int(match.group(1))
        unidade = match.group(2)
        segundos = tempo_num * 60 if unidade == 'm' else tempo_num * 3600 if unidade == 'h' else tempo_num * 86400
        if not canal:
            return await ctx.send('Escolha um canal para o sorteio acontecer.')
        if not premio:
            return await ctx.send('Nenhum prêmio especificado.')
        await ctx.send(f'*Sorteio criado {canal.mention}*')
        embed = discord.Embed(
            title='Nova oferta',
            description=f'O usuário {ctx.author.mention} está fazendo um sorteio com o prêmio de **__{premio}__**',
            color=discord.Color.blue()
        )
        embed.timestamp = discord.utils.utcnow()
        msg = await canal.send(embed=embed)
        await msg.add_reaction('🎉')
        await asyncio.sleep(segundos)
        msg = await canal.fetch_message(msg.id)  # Atualiza reações
        reaction = discord.utils.get(msg.reactions, emoji='🎉')
        if not reaction or reaction.count <= 1:
            await canal.send('Não houve pessoas suficientes para eu começar o sorteio :(')
            return
        users = [user async for user in reaction.users() if not user.bot]
        if not users:
            await canal.send('Nenhum participante válido no sorteio.')
            return
        import random
        winner = random.choice(users)
        await canal.send(f'O vencedor do sorteio para **{premio}** é... {winner.mention}! 🎉')

async def setup(bot):
    await bot.add_cog(Sorteio(bot))