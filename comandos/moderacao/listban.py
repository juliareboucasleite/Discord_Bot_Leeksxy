import discord
from discord.ext import commands

class ListBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='listban', help='Lista todos os usuários banidos do servidor e envia por DM.')
    @commands.has_permissions(ban_members=True)
    async def listban(self, ctx):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        confirm_msg = await ctx.send(f"{ctx.author.mention}, você quer receber a lista de bans? Reaja com ✅ para confirmar o envio ou ⏹ para cancelar.")
        await confirm_msg.add_reaction('✅')
        await confirm_msg.add_reaction('⏹')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['✅', '⏹'] and reaction.message.id == confirm_msg.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except Exception:
            await confirm_msg.delete()
            return

        if str(reaction.emoji) == '✅':
            try:
                bans = await ctx.guild.bans()
                if not bans:
                    await ctx.author.send('Não há usuários banidos neste servidor!')
                    await ctx.send('Nenhum usuário banido encontrado.')
                    await confirm_msg.delete()
                    return
                await ctx.send('Enviei a lista de bans no seu privado! (Se não receber, verifique suas DMs ou se não há banidos.)')
                for i, ban_entry in enumerate(bans, 1):
                    user = ban_entry.user
                    await ctx.author.send(f"{i}. **Nome:** {user} | **ID:** {user.id} | **Bot:** {user.bot}")
            except discord.Forbidden:
                await ctx.send('Não consegui enviar a lista por DM. Verifique suas configurações de privacidade.')
            except Exception as e:
                await ctx.send(f'Ocorreu um erro ao buscar a lista de bans: {e}')
        elif str(reaction.emoji) == '⏹':
            await ctx.send('O envio foi cancelado.')
        await confirm_msg.delete()

def setup(bot):
    bot.add_cog(ListBan(bot))
