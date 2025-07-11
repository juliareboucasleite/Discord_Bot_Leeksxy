import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="translate", aliases=["traduzir"])
    async def translate(self, ctx, source_lang=None, target_lang=None, *, mensagem=None):
        langs = {
            "auto": "Detectar automaticamente",
            "ar": "Árabe",
            "nl": "Holandês",
            "en": "Inglês",
            "fr": "Francês",
            "de": "Alemão",
            "el": "Grego",
            "it": "Italiano",
            "ja": "Japonês",
            "jw": "Javanês",
            "ko": "Coreano",
            "pt": "Português",
            "ro": "Romeno",
            "ru": "Russo",
            "es": "Espanhol"
        }

        if not source_lang or not target_lang or not mensagem:
            return await ctx.send("Uso: `'traduzir <de> <para> <mensagem>`\nEx: `'traduzir pt en olá mundo`")

        try:
            traduzido = GoogleTranslator(source=source_lang, target=target_lang).translate(mensagem)

            embed = discord.Embed(
                title="🌍 Google Tradutor",
                description=f"De `{langs.get(source_lang, source_lang)}` para `{langs.get(target_lang, target_lang)}`",
                color=discord.Color.blue()
            )
            embed.add_field(name="Texto original", value=mensagem, inline=False)
            embed.add_field(name="Texto traduzido", value=traduzido, inline=False)
            embed.set_footer(text=f"Requisitado por {ctx.author}", icon_url=ctx.author.display_avatar.url)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/d/db/Google_Translate_Icon.png")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro ao traduzir: `{e}`")

def setup(bot):
    bot.add_cog(Translate(bot))
