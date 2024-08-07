import discord
from discord.ext import commands

# Displays a select menu for the user to choose a channel type
class DeleteChannelSelectMenu(discord.ui.Select):
    def __init__(self, client, interaction: discord.Interaction, channel_type: str):
        # Retrieve all text or voice channels depending on the selection
        if channel_type == "text":
            channels = interaction.guild.text_channels
        elif channel_type == "voice":
            channels = interaction.guild.voice_channels
        else:
            channels = []

        # Create options for each channel
        options = [discord.SelectOption(label=channel.name, value=str(channel.id)) for channel in channels]

        # Initialize the select menu with channel options
        super().__init__(
            placeholder="Select a channel to delete",
            options=options,
            max_values=1,
        )

        self.client = client
        self.channel_type = channel_type

    # Callback function for when the user selects a channel to delete
    async def callback(self, interaction: discord.Interaction):
        channel_id = int(self.values[0])  # Get the selected channel's ID
        channel = interaction.guild.get_channel(channel_id)

        if channel:
            await channel.delete()
            await interaction.response.send_message(
                f"{self.channel_type.capitalize()} channel '{channel.name}' has been deleted.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"{self.channel_type.capitalize()} channel not found or already deleted.",
                ephemeral=True
            )

class DeleteChannelTypeSelectMenu(discord.ui.Select):
    # Initialize the select menu with options for text and voice channels
    def __init__(self, client):
        super().__init__(
            placeholder="Select Channel Type to Delete",
            options=[
                discord.SelectOption(label="Text Channel", value="text"),
                discord.SelectOption(label="Voice Channel", value="voice"),
            ],
            max_values=1,
        )

        self.client = client

    # Sends the select menu to the user when the button is clicked
    async def send_select_menu(self, interaction: discord.Interaction):
        view = discord.ui.View()
        view.add_item(self)

        # Callback function for when the user selects a channel type
        async def select_callback(interaction: discord.Interaction):
            channel_type = self.values[0]
            channel_menu = DeleteChannelSelectMenu(self.client, interaction, channel_type)
            channel_view = discord.ui.View()
            channel_view.add_item(channel_menu)
            
            await interaction.response.send_message(
                f"Select a {channel_type} channel to delete:", view=channel_view, ephemeral=True
            )

        self.callback = select_callback
        await interaction.response.send_message(
            "Select a channel type to delete:", view=view, ephemeral=True
        )
