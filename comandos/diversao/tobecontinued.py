import discord
from discord.ext import commands
from PIL import Image, ImageDraw
import requests
from io import BytesIO
from typing import Optional

class TobeContinued(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tobecontinued", aliases=["tbc", "continuado"])
    async def tbc(self, ctx, member: Optional[discord.Member] = None):
        member = member or ctx.author

        # Baixar o avatar
        avatar_url = member.display_avatar.with_format("jpg").url
        response = requests.get(avatar_url)
        avatar_img = Image.open(BytesIO(response.content)).convert("RGB")
        avatar_img = avatar_img.resize((300, 300))

        # Baixar sobreposição "to be continued"
        overlay_url = "https://i.imgur.com/sagcNyb.png"
        overlay_resp = requests.get(overlay_url)
        overlay_img = Image.open(BytesIO(overlay_resp.content)).convert("RGBA")
        overlay_img = overlay_img.resize((300, 300))

        # Combinar
        avatar_img.paste(overlay_img, (0, 0), overlay_img)

        # Enviar
        final_buffer = BytesIO()
        avatar_img.save(final_buffer, format="PNG")
        final_buffer.seek(0)
        file = discord.File(fp=final_buffer, filename="tobecontinued.png")

        await ctx.send(content=f"{ctx.author.mention}", file=file)

def setup(bot):
    bot.add_cog(TobeContinued(bot))
