import discord
from discord.ext import commands

# Displays a select menu for the user to choose a channel type
class ChannelTypeSelectModal(discord.ui.Select):
    def __init__(self, client):
        super().__init__(
            placeholder="Select Channel Type",
            options=[
                discord.SelectOption(label="None", value="none", default=True),
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
            await interaction.response.send_modal(
                ChannelNameModal(self.client, channel_type, "create")
            )

        self.callback = select_callback
        await interaction.response.send_message(
            "Select a channel type:", view=view, ephemeral=True
        )
        

# Displays a modal for the user to enter a new channel name
class ChannelNameModal(discord.ui.Modal):
    def __init__(self, client, channel_id, mode):
        super().__init__(title="Enter Channel Name")
        self.client = client
        self.channel_id = channel_id
        self.mode = mode

        self.channel_name = discord.ui.TextInput(
            label="Channel Name",
            placeholder="Enter the new channel name",
            style=discord.TextStyle.short,
            required=True,
        )
        self.add_item(self.channel_name)

    async def on_submit(self, interaction: discord.Interaction):
        name = self.channel_name.value.strip()
        guild = interaction.guild  # Get the guild from interaction

        if self.mode == "edit":
            # Find the channel by ID and rename it
            channel = guild.get_channel(self.channel_id)
            if channel:
                await channel.edit(name=name)
                await interaction.response.send_message(
                    f"Channel '{channel.name}' renamed to '{name}'.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Channel not found or unable to rename.", ephemeral=True
                )
        else:
            # Handle the creation logic if necessary
            if self.channel_id == "text":
                await guild.create_text_channel(name)
                await interaction.response.send_message(
                    f"Text channel '{name}' created.", ephemeral=True
                )
            elif self.channel_id == "voice":
                await guild.create_voice_channel(name)
                await interaction.response.send_message(
                    f"Voice channel '{name}' created.", ephemeral=True
                )
