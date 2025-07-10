import discord

# Cores minimalistas
EMBED_WHITE = 0xFFFFFF
EMBED_LIGHT_GRAY = 0xE8E8E8
EMBED_GRAY = 0xB0B0B0
EMBED_DARK_GRAY = 0x444444

def simple_embed(title: str, description: str, color=EMBED_LIGHT_GRAY):
    return discord.Embed(title=title, description=description, color=color)