import discord
from discord.ext import commands
from typing import Optional

FLIP_DICT = {
    'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ', 'f': 'ɟ', 'g': 'ƃ', 'h': 'ɥ', 'i': 'ᴉ', 'j': 'ɾ', 'k': 'ʞ', 'm': 'ɯ', 'n': 'u', 'p': 'd', 'q': 'b', 'r': 'ɹ', 't': 'ʇ', 'u': 'n', 'v': 'ʌ', 'w': 'ʍ', 'y': 'ʎ',
    'A': '∀', 'C': 'Ɔ', 'E': 'Ǝ', 'F': 'Ⅎ', 'G': 'פ', 'J': 'ſ', 'L': '˥', 'M': 'W', 'P': 'Ԁ', 'T': '┴', 'U': '∩', 'V': 'Λ', 'W': 'M', 'Y': '⅄',
    '1': 'Ɩ', '2': 'ᄅ', '3': 'Ɛ', '4': 'ㄣ', '5': 'ϛ', '6': '9', '7': 'ㄥ', '9': '6', ',': "'", '.': '˙', "'": ',', '"': ',,', '_': '‾', '&': '⅋', '!': '¡', '?': '¿', '`': ','
}

def flip_text(text: str) -> str:
    return ''.join(FLIP_DICT.get(c, c) for c in text if c is not None)

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='text', help='Converte o texto para o alfabeto invertido.')
    async def text(self, ctx, *, texto: Optional[str] = None):
        if not texto:
            await ctx.send('Forneça um texto para inverter!')
            return
        convertido = flip_text(texto)
        await ctx.send(convertido)

async def setup(bot):
    await bot.add_cog(Text(bot))
