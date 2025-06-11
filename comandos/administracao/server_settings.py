import discord
from discord.ext import commands
import sqlite3

class ServerSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def update_guild_setting(self, guild_id, setting_name, setting_value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO guild_settings (guild_id, welcome_channel_id, leave_channel_id, autorole_id)
            VALUES (?, 
                    COALESCE((SELECT welcome_channel_id FROM guild_settings WHERE guild_id = ?), ?),
                    COALESCE((SELECT leave_channel_id FROM guild_settings WHERE guild_id = ?), ?),
                    COALESCE((SELECT autorole_id FROM guild_settings WHERE guild_id = ?), ?)
                   )
        ''', (guild_id, guild_id, None, guild_id, None, guild_id, None))
        
        # Update specific setting
        if setting_name == "welcome_channel_id":
            cursor.execute("UPDATE guild_settings SET welcome_channel_id = ? WHERE guild_id = ?", (setting_value, guild_id))
        elif setting_name == "leave_channel_id":
            cursor.execute("UPDATE guild_settings SET leave_channel_id = ? WHERE guild_id = ?", (setting_value, guild_id))
        elif setting_name == "autorole_id":
            cursor.execute("UPDATE guild_settings SET autorole_id = ? WHERE guild_id = ?", (setting_value, guild_id))

        conn.commit()
        conn.close()

    def get_guild_settings(self, guild_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT welcome_channel_id, leave_channel_id, autorole_id FROM guild_settings WHERE guild_id = ?", (guild_id,))
        settings = cursor.fetchone()
        conn.close()
        return settings

    @commands.command(name="setwelcomechannel", aliases=["swc", "definircanalboasvindas", "setwc"])
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel = None):
        guild_id = ctx.guild.id
        if channel:
            self.update_guild_setting(guild_id, "welcome_channel_id", channel.id)
            embed = discord.Embed(
                title="✅ Canal de Boas-Vindas Definido!",
                description=f"O canal de boas-vindas foi definido para {channel.mention}.",
                color=0xE8E8E8
            )
        else:
            self.update_guild_setting(guild_id, "welcome_channel_id", None) # Clear setting
            embed = discord.Embed(
                title="🗑️ Canal de Boas-Vindas Removido",
                description="O canal de boas-vindas foi removido. Nenhuma mensagem será enviada.",
                color=0xE8E8E8
            )
        await ctx.send(embed=embed)

    @commands.command(name="setleavechannel", aliases=["slc", "definircanalsaida", "setlc"])
    @commands.has_permissions(administrator=True)
    async def set_leave_channel(self, ctx, channel: discord.TextChannel = None):
        guild_id = ctx.guild.id
        if channel:
            self.update_guild_setting(guild_id, "leave_channel_id", channel.id)
            embed = discord.Embed(
                title="✅ Canal de Saída Definido!",
                description=f"O canal de saída foi definido para {channel.mention}.",
                color=0xE8E8E8
            )
        else:
            self.update_guild_setting(guild_id, "leave_channel_id", None) # Clear setting
            embed = discord.Embed(
                title="🗑️ Canal de Saída Removido",
                description="O canal de saída foi removido. Nenhuma mensagem será enviada.",
                color=0xE8E8E8
            )
        await ctx.send(embed=embed)

    @commands.command(name="setautorole", aliases=["sar", "definirautorole", "setupautorole"])
    @commands.has_permissions(administrator=True)
    async def set_autorole(self, ctx, role: discord.Role = None):
        guild_id = ctx.guild.id
        if role:
            self.update_guild_setting(guild_id, "autorole_id", role.id)
            embed = discord.Embed(
                title="✅ Autorole Definido!",
                description=f"O cargo de autorole foi definido para **{role.name}**.",
                color=0xE8E8E8
            )
        else:
            self.update_guild_setting(guild_id, "autorole_id", None) # Clear setting
            embed = discord.Embed(
                title="🗑️ Autorole Removido",
                description="O cargo de autorole foi removido. Nenhum cargo será atribuído automaticamente.",
                color=0xE8E8E8
            )
        await ctx.send(embed=embed)

    @commands.command(name="showsettings", aliases=["ss", "verconfiguracoes", "viewsettings"])
    async def show_settings(self, ctx):
        guild_id = ctx.guild.id
        settings = self.get_guild_settings(guild_id)

        embed = discord.Embed(
            title="⚙️ Configurações do Servidor",
            color=0xE8E8E8
        )

        if settings:
            welcome_channel_id, leave_channel_id, autorole_id = settings
            
            welcome_channel = self.bot.get_channel(welcome_channel_id) if welcome_channel_id else "Não definido"
            leave_channel = self.bot.get_channel(leave_channel_id) if leave_channel_id else "Não definido"
            autorole = ctx.guild.get_role(autorole_id) if autorole_id else "Não definido"

            embed.add_field(name="Bem-Vindo Canal", value=welcome_channel.mention if isinstance(welcome_channel, discord.TextChannel) else welcome_channel, inline=False)
            embed.add_field(name="Sair Canal", value=leave_channel.mention if isinstance(leave_channel, discord.TextChannel) else leave_channel, inline=False)
            embed.add_field(name="Autorole", value=autorole.mention if isinstance(autorole, discord.Role) else autorole, inline=False)
        else:
            embed.description = "Nenhuma configuração encontrada para este servidor."

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerSettings(bot)) 