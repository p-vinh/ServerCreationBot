import discord
import asyncio
from ChannelCreationModal import ChannelTypeSelectModal
from ChannelEdit import ChannelEditModal

# This class creates a menu with three buttons: Create Channel, Edit Channel, and Delete Channel
class MenuButtons(discord.ui.View):
    def __init__(self, client):
        super().__init__()
        self.client = client
        
    # Separate the buttons into different functions for better organization

    # Discord UI buttons for the Creating a Channel
    @discord.ui.button(label="Create Channel", style=discord.ButtonStyle.primary)
    async def create_channel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ChannelTypeSelectModal(self.client) # Create a new instance of the ChannelTypeSelectModal class
        await modal.send_select_menu(interaction)
        
    # Discord UI buttons for the Editing a Channel
    @discord.ui.button(label="Edit Channel", style=discord.ButtonStyle.secondary)
    async def edit_channel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ChannelEditModal(self.client, interaction)
        await modal.send_select_menu(interaction)
    
    # Discord UI buttons for the Deleting a Channel
    @discord.ui.button(label="Delete Channel", style=discord.ButtonStyle.danger)
    async def delete_channel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Delete Channel")