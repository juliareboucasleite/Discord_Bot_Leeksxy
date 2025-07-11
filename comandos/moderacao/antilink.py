import discord
from discord.ext import commands
from comandos.moderacao.server_settings import ServerSettings

class AntiLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Acesso ao cog de configurações
        self.server_settings: ServerSettings = bot.get_cog('ServerSettings')

    @commands.command(name='antilink', aliases=['antipalavrao'])
    @commands.has_permissions(manage_messages=True)
    async def antilink(self, ctx):
        guild_id = ctx.guild.id
        # Buscar status atual
        status = self.server_settings.get_antilink_status(guild_id)
        status_str = 'ligado.' if status == 'on' else 'desligado.'

        embed = discord.Embed(
            title='🛸 | Anti-{link/palavrão}',
            description='Use as reações para tais funções:\n>>> 🔵 = ligado\n🔴 = desligado',
            color=discord.Color.blue() if status == 'on' else discord.Color.red()
        )
        embed.set_footer(text=f'Anti-{{link/palavrão}}: {status_str}')

        msg = await ctx.send(embed=embed)
        await msg.add_reaction('🔵')
        await msg.add_reaction('🔴')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['🔵', '🔴'] and reaction.message.id == msg.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except Exception:
            return

        if str(reaction.emoji) == '🔵':
            self.server_settings.update_antilink_status(guild_id, 'on')
            embed.set_footer(text='Anti-{link/palavrão}: ligado.')
            embed.color = discord.Color.blue()
            await msg.edit(embed=embed)
        elif str(reaction.emoji) == '🔴':
            self.server_settings.update_antilink_status(guild_id, 'off')
            embed.set_footer(text='Anti-{link/palavrão}: desligado.')
            embed.color = discord.Color.red()
            await msg.edit(embed=embed)
        try:
            await msg.clear_reactions()
        except Exception:
            pass

async def setup(bot):
    await bot.add_cog(AntiLink(bot))
