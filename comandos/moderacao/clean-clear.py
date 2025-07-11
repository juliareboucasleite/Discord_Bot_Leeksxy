import discord
from discord.ext import commands
from typing import Optional

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipes = {}  # channel_id: {'author': str, 'content': str, 'image': Optional[str]}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        snipe_data = {
            'author': str(message.author),
            'content': message.content,
            'image': message.attachments[0].url if message.attachments else None
        }
        self.snipes[message.channel.id] = snipe_data

    @commands.command(name='snipe', aliases=['ms', 'messagesnipe'], help='Mostra a última mensagem deletada deste canal.')
    async def snipe(self, ctx):
        snipe = self.snipes.get(ctx.channel.id)
        if not snipe:
            await ctx.send('Não há mensagens excluídas neste canal!')
            return
        embed = discord.Embed(
            description=snipe['content'] or '*Sem texto*',
            color=discord.Color.orange()
        )
        embed.set_author(name=snipe['author'])
        if snipe['image']:
            embed.set_image(url=snipe['image'])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Snipe(bot))
