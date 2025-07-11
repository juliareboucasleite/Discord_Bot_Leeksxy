import discord
from discord.ext import commands

class VoiceInvite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='voiceinvite', aliases=['voice-invite'], help='Convida usuários mencionados para seu canal de voz privado.')
    async def voiceinvite(self, ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            msg = await ctx.send('Você precisa estar em um canal de voz para usar este comando.')
            await ctx.message.delete()
            await msg.delete(delay=1.5)
            return
        channel = ctx.author.voice.channel
        if not channel.name.startswith('⌛'):
            await ctx.send('Este comando só pode ser usado em canais privados (nome iniciando com ⌛).')
            return
        mentions = ctx.message.mentions
        if not mentions:
            await ctx.send('Mencione os usuários que deseja convidar.')
            return
        allow_list = []
        for user in mentions:
            allow_list.append(discord.PermissionOverwrite(connect=True))
            await channel.set_permissions(user, connect=True)
        done_msg = await ctx.send(f'Hey! {ctx.author.display_name}, adicionei os citados à sua lista de convidados.')
        await ctx.message.delete()
        await done_msg.delete(delay=2)

async def setup(bot):
    await bot.add_cog(VoiceInvite(bot))