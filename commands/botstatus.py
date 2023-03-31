import nextcord




async def bot_status(interaction: nextcord.Interaction):
    # Check if bot is online or offline
    if nextcord.bot.is_closed():
        status = "Offline"
    else:
        status = "Online"
    
    # Create embed with bot status
    embed = nextcord.Embed(title="Bot Status", color=0xFF5733)
    embed.add_field(name="Status", value=status)
    
    # Send the embed as a response
    await interaction.response.send_message(embed=embed)
