import discord
import asyncio
from ChannelCreationModal import ChannelTypeSelectModal
from DeleteChannel import DeleteChannelTypeSelectMenu

class MenuButtons(discord.ui.View):
    def __init__(self, client):
        super().__init__()
        self.client = client

    @discord.ui.button(label="Create Channel", style=discord.ButtonStyle.primary)
    async def create_channel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ChannelTypeSelectModal(self.client)
        await modal.send_select_menu(interaction)
        
    @discord.ui.button(label="Edit Channel", style=discord.ButtonStyle.secondary)
    async def edit_channel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Edit Channel")
        
    @discord.ui.button(label="Delete Channel", style=discord.ButtonStyle.danger)
    async def delete_channel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        delete_menu = DeleteChannelTypeSelectMenu(self.client)
        await delete_menu.send_select_menu(interaction)