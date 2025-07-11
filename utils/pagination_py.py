import discord
from discord.ext import commands

async def paginate(ctx, pages, emoji_list=None, timeout=120):
    if emoji_list is None:
        emoji_list = ["◀️", "⏹️", "▶️"]

    if not ctx or not ctx.channel:
        raise Exception("Canal inacessível.")
    if not pages:
        raise Exception("Páginas não fornecidas.")

    page = 0
    message = await ctx.send(
        embed=pages[page].set_footer(
            text=f"Página {page + 1}/{len(pages)}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
    )

    for emoji in emoji_list:
        await message.add_reaction(emoji)

    def check(reaction, user):
        return (
            user == ctx.author
            and str(reaction.emoji) in emoji_list
            and reaction.message.id == message.id
        )

    while True:
        try:
            reaction, user = await ctx.bot.wait_for("reaction_add", timeout=timeout, check=check)
        except Exception:
            break

        if str(reaction.emoji) == emoji_list[0]:  # Anterior
            page = page - 1 if page > 0 else len(pages) - 1
        elif str(reaction.emoji) == emoji_list[1]:  # Parar
            await message.clear_reactions()
            break
        elif str(reaction.emoji) == emoji_list[2]:  # Próxima
            page = page + 1 if page + 1 < len(pages) else 0

        await message.edit(
            embed=pages[page].set_footer(
                text=f"Página {page + 1}/{len(pages)}",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None
            )
        )
        await message.remove_reaction(reaction.emoji, ctx.author)

    try:
        await message.clear_reactions()
    except Exception:
        pass

    return message 