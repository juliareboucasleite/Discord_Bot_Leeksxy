import discord
from discord.ext import commands
import re
from typing import Optional

class ShowEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='showemoji', aliases=['bigemoji'], help='Mostra o emoji enviado em tamanho grande.')
    async def showemoji(self, ctx, emoji: Optional[str] = None):
        if not emoji:
            await ctx.send('Por favor, envie um emoji!')
            return
        # Tenta identificar se é um emoji customizado do Discord
        custom_emoji = re.match(r'<a?:([a-zA-Z0-9_]+):(\d+)>', emoji)
        if custom_emoji:
            emoji_id = custom_emoji.group(2)
            animated = emoji.startswith('<a:')
            ext = 'gif' if animated else 'png'
            url = f'https://cdn.discordapp.com/emojis/{emoji_id}.{ext}'
            embed = discord.Embed(title='Emoji:', color=discord.Color.blurple())
            embed.set_image(url=url)
            await ctx.send(embed=embed)
            return
        # Tenta identificar se é um emoji unicode
        try:
            codepoint = '-'.join(f'{ord(c):x}' for c in emoji)
            url = f'https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/72x72/{codepoint}.png'
            embed = discord.Embed(title='Emoji:', color=discord.Color.blurple())
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send('Mande um emoji válido!')

def setup(bot):
    bot.add_cog(ShowEmoji(bot))
