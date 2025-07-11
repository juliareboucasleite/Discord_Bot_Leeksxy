import discord
from discord.ext import commands
from comandos.moderacao.server_settings import ServerSettings
from typing import Optional

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_settings: ServerSettings = bot.get_cog('ServerSettings')

    @commands.command(name='config', aliases=['conf'])
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        guild_id = ctx.guild.id
        prefix = self.server_settings.get_prefix(guild_id)
        dj_role_id = self.server_settings.get_dj_role(guild_id)
        dj_role = ctx.guild.get_role(dj_role_id) if dj_role_id else None

        embed = discord.Embed(
            title='⚙️ Configurações do Bot',
            color=0x7289DA
        )
        embed.add_field(name='Prefixo', value=f'`{prefix}`', inline=True)
        embed.add_field(name='DJ Role', value=dj_role.mention if dj_role else 'Não definido', inline=True)
        embed.description = 'Reaja para editar:\n:one: - Prefixo\n:two: - Cargo DJ'
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('1️⃣')
        await msg.add_reaction('2️⃣')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['1️⃣', '2️⃣'] and reaction.message.id == msg.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except Exception:
            await msg.clear_reactions()
            return

        if str(reaction.emoji) == '1️⃣':
            await msg.clear_reactions()
            await ctx.send('Digite o novo prefixo (máx. 3 caracteres):')
            def msg_check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                resposta = await self.bot.wait_for('message', timeout=30.0, check=msg_check)
            except Exception:
                return await ctx.send('Tempo esgotado para definir o prefixo.')
            novo_prefixo = resposta.content.strip()
            if len(novo_prefixo) > 3:
                return await ctx.send('O prefixo deve ter no máximo 3 caracteres.')
            self.server_settings.update_prefix(guild_id, novo_prefixo)
            await ctx.send(f'Prefixo atualizado para `{novo_prefixo}` com sucesso!')
        elif str(reaction.emoji) == '2️⃣':
            await msg.clear_reactions()
            await ctx.send('Mencione o novo cargo DJ:')
            def role_check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.role_mentions
            try:
                resposta = await self.bot.wait_for('message', timeout=30.0, check=role_check)
            except Exception:
                return await ctx.send('Tempo esgotado para definir o cargo DJ.')
            novo_role = resposta.role_mentions[0]
            self.server_settings.update_dj_role(guild_id, novo_role.id)
            await ctx.send(f'Cargo DJ atualizado para {novo_role.mention} com sucesso!')

async def setup(bot):
    await bot.add_cog(Config(bot))
