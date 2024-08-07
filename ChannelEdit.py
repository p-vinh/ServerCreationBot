import discord
from ChannelCreationModal import ChannelNameModal

# Displays a modal for the user to select a channel to edit
class ChannelEditModal(discord.ui.Select):
    def __init__(self, client, interaction):
        # Super call with appropriate parameters for initializing select options
        super().__init__(
            placeholder="Select Channel to Edit",
            max_values=1
        )
        self.client = client
        self.interaction = interaction

        # Find all existing channels in the guild
        # Sort the channels by text and voice
        text_channels = []
        voice_channels = []
        
        for guild in self.client.guilds:
            if guild.id == interaction.guild_id:  # Use the correct guild
                for channel in guild.text_channels:
                    text_channels.append(
                        discord.SelectOption(label=channel.name, value=str(channel.id))
                    )
                for channel in guild.voice_channels:
                    voice_channels.append(
                        discord.SelectOption(label=channel.name, value=str(channel.id))
                    )

        # Join both text and voice channels into one list
        self.options = text_channels + voice_channels

    async def send_select_menu(self, interaction: discord.Interaction):
        view = discord.ui.View()
        view.add_item(self)

        # Set the callback correctly
        self.callback = self.select_callback
        
        await interaction.response.send_message(
            "Select a channel to edit:", view=view, ephemeral=True
        )

    async def select_callback(self, interaction: discord.Interaction):
        # Get the selected channel ID
        channel_id = int(self.values[0])  # Make sure to convert to int
        await interaction.response.send_modal(
            ChannelNameModal(self.client, channel_id, "edit")
        )
