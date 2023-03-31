# Import necessary modules
from nextcord.components import Component,Button
import wikipediaapi
import string
import base64
from typing import Optional
from typing import Dict, Union
import asyncio
import json
import feedparser
import requests
import openai
import random
import datetime
import nextcord
from nextcord import Colour, Embed, Interaction, SelectMenu, SelectOption, SlashCommandOption, SlashOption, slash_command
from nextcord.ext import commands
from datetime import datetime, timedelta
from nextcord import Activity, ActivityType
from nextcord.ext import commands
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pathlib import Path
from dateutil import parser
from dateutil.parser import parse as parse_duration
from nextcord import SelectOption, SelectMenu, ui
from typing import List
from mcstatus import JavaServer
from nextcord.ext.commands import Cog
import io
import functools
from functools import partial
import re
from nextcord.ui import Button, View




# opennai stuff
openai_model_engine = "text-davinci-003" # You can change this to another OpenAI model engine if you'd like
openai.api_key = "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"




"""
This is for anytime we need a client event
(client.event)
"""
client = nextcord.Client()
interaction_responded = False








# Creates a new instance of the bot class
intents = nextcord.Intents.all()
intents.guild_messages = True

bot = commands.Bot(command_prefix='/', intents=nextcord.Intents.all())
















# Define a list of tracked activities
TRACKED_ACTIVITIES = ['message', 'command', 'voice']

# Define a time interval for tracking
TRACKING_INTERVAL = timedelta(days=7)

# Define the colors for the graph
GRAPH_COLORS = ['r', 'g', 'b']

# Define the title and description for the embed message
EMBED_TITLE = 'User Stats'
EMBED_DESCRIPTION = 'User activity stats for the past week:'
# Define a dictionary to store log channel information
log_channels = {}



# A list of banned words
banned_words = ['spam', 'scam', 'bot']













# maybe delete this one? 

openai.api_key = "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"

messages_in_channel = []
messages_in_dm = []
conversations = {}

# this logs the changelog 
with open("changelog.txt", "r") as f:
    changelog = f.read()

changelog_channel_id = 1081786980729356288
# this is the end, dont mess with this code
# Replace CHANNEL_ID with the ID of the channel where you want to send the updates


# Dictionary to track user points
user_points = {}








# Create the suggestion channel and log channel
async def setup(guild: nextcord.Guild):
    # Create the suggestion channel
    suggestion_channel = await guild.create_text_channel('suggestions')
    await suggestion_channel.set_permissions(guild.default_role, send_messages=False)

    # Create the suggestion log channel
    suggestion_log_channel = await guild.create_text_channel('suggestion-log')
    await suggestion_log_channel.set_permissions(guild.default_role, read_messages=False)

    return suggestion_channel, suggestion_log_channel

# when the bot logs on, displays this the message in the terminal!















    





















async def create_role_button_callback(interaction: nextcord.Interaction, role):
    if role in interaction.user.roles:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(f"{role.name} role removed!", ephemeral=True)
    else:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"{role.name} role added!", ephemeral=True)







"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""



@bot.event
async def on_ready():
    # Set the bot's status to "listening to what the people want!"
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="to what the people want!"))
    
    # Log in the console that the bot has successfully logged in
    print('Logged in as {0.user}'.format(bot))
    
    # Get the changelog channel object
    changelog_channel = bot.get_channel(changelog_channel_id)
    
    # Delete the most recent changelog message in the channel
    async for message in changelog_channel.history(limit=1):
        await message.delete()
        
    # Send the new changelog message to the channel
    embed = nextcord.Embed(title="Changelog for Wadder", description=changelog, color=0xFF5733)
    embed.add_field(name="Developer", value="Wade#1781", inline=False)
    await changelog_channel.send(embed=embed)




 
 

@bot.event
async def on_message(message: nextcord.Message):
    # Ignore messages sent by the bot
    if message.author.bot:
        return

    # Log the message to a file
    log_file = "message_log.txt"
    with open(log_file, "a") as f:
        f.write(f"{message.guild.name} - {message.channel.name} - {message.author.name}#{message.author.discriminator}: {message.content}\n")





# THIS IS ROUGH sstil something wrong with the code but works


@bot.slash_command(name="help",description="Shows a list of available commands")
async def help33333(interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):
    # List of commands to display in the embed
    command_list = [
("/add", "Calculate the sum of two numbers"),
("/add_role", "Add a role to a user in the server"),
("/advertise", "Advertise the bot and its features"),
("/advertiseYOU", "Advertise your server in a linked channel"),
("/ban", "Ban a user from the server"),
("/calculate_average", "Calculate the average of a list of numbers"),
("/celsius", "Convert a temperature from Celsius to Fahrenheit"),
("/chatbot", "Chat with the OpenAI chatbot"),
("/chucknorris", "Get a random Chuck Norris joke"),
("/clear", "Deletes a specified number of messages from a channel"),
("/codeblock", "Return the input text as a code block"),
("/countdown", "Countdown to a specified event"),
("/define", "Get the definition of a word from the Merriam-Webster dictionary"),
("/deafen", "Deafen a user in a voice channel"),
("/encrypt_caesar", "Encrypt text using the Caesar cipher"),
("/flip", "Flip a coin"),
("/game_deals", "Sends a notification to the specified channel with details about any free or discounted games on Steam"),
("/game_deals2", "Sends a notification with details about any free or discounted games on Steam"),
("/generate_code2", "Generate code snippets using the Davinci 003 engine"),
("/generate_financial_advice", "Generate personalized financial advice using the Davinci 003 engine. This is for fun not to be used for real life!"),
("/generate_legal_document", "Generate legal documents using the Davinci 003 engine. Not true legal advice!"),
("/generate_lyrics", "Generate song lyrics using the Davinci 003 engine"),
("/generate_poem", "Generate a poem using the Davinci 003 engine"),
("/generate_product_name", "Generate a unique product name using the Davinci 003 engine"),
("/generate_program", "Generate a complex software program using the Davinci 003 engine"),
("/generate_story", "Generate a short story using the Davinci 003 engine"),
("/generate_technical_documentation", "Generate technical documentation using the Davinci 003 engine"),
("/horoscope", "Provides daily horoscope for the user's zodiac sign"),
("/kick", "Kick a user from the server"),
("/lock", "Locks a channel to prevent users from sending messages"),
("/lyrics", "Get the lyrics of a song"),
("/mute", "Mute a user in the server"),
("/mutevoice", "Mute a user in a voice channel"),
("/nickname", "Changes the nickname of a user on the server"),
("/ping", "Ping the bot to test its responsiveness"),
("/progjoke", "Get a random programming joke"),
("/quote_text", "Format text as a quote"),
("/random_quote", "Get a random quote"),
("/remind2", "Set a reminder message to repeat in a set amount of hours"),
("/remove_role", "Remove a role from a user in the serve"),
("/reverse", "Reverse a message"),
("/roll", "Roll some dice"),
("/send_news", "Send news updates to a specified channel"),
("/send_rules", "admin custom rules"),
("/serverinfo", "Display information about the server"),
("/setup_logging", "Logging channel set up"),
("/slowmode", "Sets the slowmode delay for a channel"),
("/suggest3", "Submit a suggestion"),
("/suggest4", "Submit a suggestion2"),
("/summarize", "Summarize text using the Davinci 003 engine"),
("/talk2", "Make the bot talk in a channel"),
("/tempban", "Temporarily bansa user from the server"),
("/translate", "Translate text to another language using Google Translate"),
("/unban", "Unban a user from the server"),
("/undeafen", "Undeafen a user in a voice channel"),
("/unlock", "Unlocks a locked channel"),
("/unmute", "Unmute a user in the server"),
("/unmutevoice", "Unmute a user in a voice channel"),
("/uptime", "Get the uptime of the bot"),
("/urban", "Get the definition of a word from the Urban Dictionary"),
("/usercount", "Get the number of users in the server"),
("/weather", "Get the current weather for a specified location"),
("/wiki", "Get a summary of a Wikipedia article"),
("/wolfram", "Get the answer to a question using Wolfram Alpha"),
("/youtube", "Search for a video on YouTube"),
("/ytstats", "Get statistics about a YouTube channel")




    ]

    # Divide the commands into pages of 10 commands each
    pages = [command_list[i:i + 10] for i in range(0, len(command_list), 10)]

    # Create an embed for each page of commands
    embeds = []
    for i, page in enumerate(pages):
        embed = nextcord.Embed(title=f"Page {i + 1}/{len(pages)}", color=0x7289da)
        for command, description in page:
            embed.add_field(name=command, value=description, inline=False)
        embeds.append(embed)

    # Create a view with buttons to navigate between pages
    view = nextcord.ui.View()
    for i in range(len(embeds)):
        button = nextcord.ui.Button(style=nextcord.ButtonStyle.secondary, label=str(i + 1))
        button.callback = partial(on_help_button_click, embeds, i, Interaction)
        view.add_item(button)

    # Send the first page of commands with the view
    await interaction.response.send_message(embed=embeds[0], view=view)

async def on_help_button_click(embeds, page_index, button, interaction):
    # Update the message with the embed for the clicked page
    message = interaction.message
    await message.edit(embed=embeds[page_index])
    # Update the style of the clicked button to indicate that it is selected
    for item in interaction.message.components[0].children:
        if isinstance(item, nextcord.ui.Button) and item.label == button.label:
            item.style = nextcord.ButtonStyle.primary
        else:
            item.style = nextcord.ButtonStyle.secondary
    message: nextcord.Message = interaction.message
    await interaction.edit_original_message(content=[interaction.message.components[0]])









# fucking works



@bot.slash_command(name='setuput', description='Sets up welcome and leave channels.')
async def setup(interaction: nextcord.Interaction, welcome_message: str, leave_message: str):
    guild = interaction.guild
    welcome_channel = await guild.create_text_channel('welcome')
    leave_channel = await guild.create_text_channel('leave')

    # set up welcome channel
    welcome_msg = await welcome_channel.send(welcome_message)

    # set up leave channel
    leave_msg = await leave_channel.send(leave_message)

    # set up server settings
    settings = {
        'welcome_channel': welcome_channel.id,
        'leave_channel': leave_channel.id,
        'welcome_message': welcome_message,
        'leave_message': leave_message
    }
    
    # save server settings to a file
    with open(f'{guild.id}_server_settings.txt', 'w') as f:
        f.write(str(settings))

    async def on_member_join(member):
        welcome_channel = member.guild.get_channel(settings['welcome_channel'])
        if welcome_channel:
            welcome_members = [m.name for m in welcome_channel.members]
            welcome_members.append(member.name)
            welcome_content = f"{settings['welcome_message']}\n"
            if welcome_members:
                welcome_content += "\n".join(welcome_members)
            await welcome_msg.edit(content=welcome_content)

            embed = Embed(title=f"{member.name} joined the server", color=0x00FF00)
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Welcome!", value=f"Please welcome {member.mention} to the server!")
            await welcome_channel.send(embed=embed)

    async def on_member_remove(member):
        leave_channel = member.guild.get_channel(settings['leave_channel'])
        if leave_channel:
            left_members = [m.name for m in leave_channel.members]
            left_members.append(member.name)
            leave_content = f"{settings['leave_message']}\n"
            if left_members:
                leave_content += "\n".join(left_members)
            await leave_msg.edit(content=leave_content)

            embed = Embed(title=f"{member.name} left the server", color=0xFF0000)
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Goodbye!", value=f"We're sorry to see {member.mention} go.")
            await leave_channel.send(embed=embed)

    bot.add_listener(on_member_join, 'on_member_join')
    bot.add_listener(on_member_remove, 'on_member_remove')

    await interaction.response.send_message("Setup complete.", ephemeral=True)








"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

@bot.slash_command(description="Say hello to the bot")
async def hello(interaction: Interaction):
    await interaction.response.send_message("Hello!")








"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# current time command

@bot.slash_command(description="Get the current time")
async def time(interaction: Interaction):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    await interaction.response.send_message(f"The current time is {current_time}")





"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# roll dice command

@bot.slash_command(description="Roll some dice")
async def roll(interaction: Interaction, num_dice: int):
    if num_dice < 1:
        await interaction.response.send_message("Please specify a positive number of dice to roll.")
        return
    dice = [random.randint(1, 6) for _ in range(num_dice)]
    response = f"Rolling {num_dice} dice: {', '.join(str(die) for die in dice)}"
    await interaction.response.send_message(response)









"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# flip a coin

@bot.slash_command(description="Flip a coin")
async def flip(interaction: Interaction):
    result = random.choice(["heads", "tails"])
    await interaction.response.send_message(f"The coin landed on {result}!")










"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# works but add a template to the server settings, (make it save in a embed and file send to the channel as a .txt file)
@bot.command(name="savetemplate")
async def save_template(message, name=None, channel=None):
    """
    Saves the current server as a template and sends it as a message to a specified channel.
    """
    if name is None:
        name = "My Server Template"
    
    template = await message.guild.create_template(name=name)
    
    if channel is not None:
        channel_obj = bot.get_channel(int(channel))
        if channel_obj is not None:
            await channel_obj.send(f"The server template '{name}' has been created. You can find it under Server Settings > Templates.", file=nextcord.File(await template.use()))
        else:
            await message.channel.send("Invalid channel ID.")
    else:
        await message.channel.send(f"The server template '{name}' has been created. You can find it under Server Settings > Templates.", file=nextcord.File(await template.use()))












"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# Defines the fucntion to handle the ping command

@bot.slash_command(description="Ping command")
async def ping(interaction: Interaction):
    # Calculate the bot's websocket latency
    latency = bot.latency * 1000  # in milliseconds

    # Define the embed
    embed = nextcord.Embed(title="Ping", color=0xFF5733)
    embed.add_field(name="Latency", value=f"{latency:.2f} ms")

    # Define the button to refresh the ping
    async def refresh_callback(interaction: nextcord.Interaction):
        await interaction.response.edit_message(embed=embed)

    refresh_button = nextcord.ui.Button(label="Refresh", style=nextcord.ButtonStyle.secondary)
    refresh_button.callback = refresh_callback

    # Send the embed with the refresh button as a response
    view = nextcord.ui.View()
    view.add_item(refresh_button)

    await interaction.response.send_message(embed=embed, view=view)









"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# works, untill gets to the nextcordbot interg

from commands.botstatus import bot_status
@bot.slash_command(name="bot_status", description="Display Information about the the bot")
async def botstatus(interaction: nextcord.Interaction):
    await bot_status(interaction)




"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# working for server (each server)

from commands.serverinfo import serverinfo


@bot.slash_command(name="serverinfo", description="Display Information about the Server")
async def serverinformation(interaction: nextcord.Interaction):
    await serverinfo(interaction)


"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# openai chatbot within discord #

from commands.chatbot import chatbot

@bot.slash_command(name="chatbot", description="Chat with an AI bot")
async def chatbot_command(interaction: nextcord.Interaction):
    await chatbot(interaction, bot)





"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

# first command that is in a folder #
from commands.random_quote import random_quotes

@bot.slash_command(description="Get a random quote")
async def fetch_random_quote(interaction: nextcord.Interaction):
    await random_quotes(interaction)


"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# servers with the wadder bot #

from commands.servers import serverswbot

@bot.slash_command(description="The Servers that Wadder is in!")
async def fetch_serverswbot(interaction: nextcord.Interaction):
    await serverswbot(interaction)







"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

# very good

@bot.command()
async def ticket4(ctx):
    # Create a category for the ticket channels
    category_name = "Tickets"
    category = await ctx.guild.create_category(category_name)

    # Create a new ticket channel
    ticket_channel_name = f"ticket-{ctx.author.name}"
    overwrites = {
        ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
        ctx.author: nextcord.PermissionOverwrite(read_messages=True, send_messages=True),
        bot.user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    ticket_channel = await ctx.guild.create_text_channel(ticket_channel_name, category=category, overwrites=overwrites)

    # Add reaction to the ticket message
    message = await ticket_channel.send(f"{ctx.author.mention} created a new ticket. React with 👍 to claim it!")
    await message.add_reaction("👍")

    # Wait for a reaction to the ticket message
    def check(reaction, user):
        return user != bot.user and reaction.message == message and str(reaction.emoji) == "👍"

    try:
        reaction, user = await bot.wait_for('reaction_add', check=check, timeout=3600.0)
    except asyncio.TimeoutError:
        await ticket_channel.send("This ticket has been closed due to inactivity.")
        await category.delete()
        return

    # Create a new ticket channel for the admin and the user who claimed the ticket
    claimed_by = user
    overwrites = {
        ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
        ctx.author: nextcord.PermissionOverwrite(read_messages=True, send_messages=True),
        bot.user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True),
        claimed_by: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    ticket_channel_name = f"ticket-{ctx.author.name}-{claimed_by.name}"
    ticket_channel = await ctx.guild.create_text_channel(ticket_channel_name, category=category, overwrites=overwrites)

    # Notify the admin and the user who claimed the ticket
    await ticket_channel.send(f"{ctx.author.mention} and {claimed_by.mention} are now in a private chat.")









"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

# Good Ticket System, one or two things need to find change
@bot.command()
async def ticket2(ctx):
    # Send a DM to the user to get information about the ticket
    dm_channel = await ctx.author.create_dm()
    await dm_channel.send("What is this ticket for?")

    while True:
        def check(m):
            return m.author == ctx.author and isinstance(m.channel, nextcord.DMChannel)

        # Wait for the user to respond in DM
        try:
            issue = await bot.wait_for('message', check=check, timeout=300.0)
        except asyncio.TimeoutError:
            await dm_channel.send("You took too long to respond. Please use the !ticket command again.")
            return

        issue_description = issue.content

        # Create a new ticket channel
        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            ctx.author: nextcord.PermissionOverwrite(read_messages=True, send_messages=True),
            bot.user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        new_channel = await ctx.guild.create_text_channel(name=f"ticket-{ctx.author.name}", overwrites=overwrites)

        # Send a message to the new ticket channel and an announcement channel
        select_channel = bot.get_channel(1061743622376140892)
        ticket_channel = bot.get_channel(new_channel.id)

        await select_channel.send(f"New ticket from {ctx.author.mention} regarding {issue_description}")
        await select_channel.send(f"Ticket channel: {ticket_channel.mention}")

        await ticket_channel.send(f"New ticket from {ctx.author.mention} regarding {issue_description}")

        # Wait for a response in the new ticket channel
        def check_response(m):
            return m.channel == new_channel and m.author != bot.user

        while True:
            try:
                response = await bot.wait_for('message', check=check_response, timeout=600.0)
            except asyncio.TimeoutError:
                await new_channel.send("This ticket has been closed due to inactivity.")
                await select_channel.send(f"Ticket from {ctx.author.mention} regarding {issue_description} has been closed.")
                break

            # Forward the response to the announcement channel
            await select_channel.send(f"{response.author.mention} in {ticket_channel.mention}: {response.content}")

            # Send response to the user in DM
            await dm_channel.send(f"{response.author.mention} in {ticket_channel.mention}: {response.content}")
    



#######################################################


@bot.slash_command(name="create_role_buttons")
async def create_role_buttons(interaction: nextcord.Interaction, roles: str):
    await interaction.response.send_message("Creating role buttons...", ephemeral=True)

    role_ids = [int(role_id) for role_id in nextcord.utils.find_all(nextcord.Role.mention_regex(), roles)]
    role_list = [interaction.guild.get_role(role_id) for role_id in role_ids]

    view = View()
    for role in role_list:
        role_button = Button(label=role.name, custom_id=f"role:{role.id}")
        view.add_item(role_button)

    message_text = "Click a button to get or remove the corresponding role:"
    message = await interaction.channel.send(message_text, view=view)

@bot.event
async def on_interaction(interaction: nextcord.Interaction):
    if interaction.type == nextcord.InteractionType.component and interaction.custom_id.startswith("role:"):
        role_id = int(interaction.custom_id.split(":")[1])
        role = interaction.guild.get_role(role_id)
        await create_role_button_callback(interaction, role)


















"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

# Rules for all servers! EZ

@bot.command(name='rules')
async def send_rules(ctx):
    channel_name_message = await ctx.send('Please enter the name of the channel you want to send the rules to:')

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        channel_name = await bot.wait_for('message', check=check, timeout=60)
    except nextcord.TimeoutError:
        await ctx.send('You took too long to respond.')
        return

    await ctx.send('Please enter the rules, one by one. Type `done` when you are finished.')

    rules = []
    while True:
        try:
            rule_message = await bot.wait_for('message', check=check, timeout=60)
        except nextcord.TimeoutError:
            await ctx.send('You took too long to respond.')
            return

        if rule_message.content.lower() == 'done':
            break

        rules.append(rule_message.content)

    channel = nextcord.utils.get(ctx.guild.channels, name=channel_name.content)

    if channel is None:
        await ctx.send('Channel not found.')
        return

    # Create the embed
    embed = nextcord.Embed(title='Server Rules')
    for i, rule in enumerate(rules):
        embed.add_field(name=f'Rule {i+1}:', value=rule, inline=False)

    # Send the embed to the specified channel
    await channel.send(embed=embed)

    await ctx.send('Rules sent to ' + channel_name.content + '.')









"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

# Logger Channel Command EZ FOR USER

@bot.command()
async def setlogchannel(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    await ctx.send("Please enter the ID of the channel to log events to:")
    channel_id_msg = await bot.wait_for('message', check=check)

    channel = bot.get_channel(int(channel_id_msg.content))
    if channel is None:
        await ctx.send("Invalid channel ID, please try again.")
        return

    await ctx.send(f"Log channel set to {channel.mention}.")

    # Store the channel ID in a variable for later use
    log_channel_id = channel.id

    # Define the log embed
    log_embed = nextcord.Embed(title="Message Log", color=0x00ff00)

    # Set up the event listeners for message sending, editing, and deletion
    @bot.listen('on_message')
    async def on_message(message):
        # Check if the message is from a bot to avoid logging bot messages
        if message.author.bot:
            return

        # Add a message sent entry to the log embed
        log_embed.add_field(name="Message Sent", value=f"{message.author.mention} sent a message in {message.channel.mention}:\n{message.content}", inline=False)

        # Send the log embed to the log channel
        log_channel = bot.get_channel(log_channel_id)
        await log_channel.send(embed=log_embed)

    @bot.listen('on_message_edit')
    async def on_message_edit(before, after):
        # Check if the message is from a bot to avoid logging bot messages
        if before.author.bot:
            return

        # Add a message edited entry to the log embed
        log_embed.add_field(name="Message Edited", value=f"{before.author.mention} edited their message in {before.channel.mention} from:\n{before.content}\nTo:\n{after.content}", inline=False)

        # Send the log embed to the log channel
        log_channel = bot.get_channel(log_channel_id)
        await log_channel.send(embed=log_embed)

    @bot.listen('on_message_delete')
    async def on_message_delete(message):
        # Check if the message is from a bot to avoid logging bot messages
        if message.author.bot:
            return

        # Add a message deleted entry to the log embed
        log_embed.add_field(name="Message Deleted", value=f"{message.author.mention} deleted their message in {message.channel.mention}:\n{message.content}", inline=False)

        # Send the log embed to the log channel
        log_channel = bot.get_channel(log_channel_id)
        await log_channel.send(embed=log_embed)









"""
This is the warn command (Ready To GO)
 
"""

@bot.slash_command(description="Issues a warning to a user.")
async def warn(interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided."):
    """
    Issues a warning to a user.

    Args:
        - user (nextcord.Member): The member to warn.
        - reason (str): The reason for the warning.
    """
    # Check if the user has permission to warn
    if not interaction.user or not isinstance(interaction.user, nextcord.Member) or not interaction.user.guild_permissions.kick_members:
        return await interaction.response.send_message("You do not have permission to warn members.")

    # Warn the user
    await interaction.response.send_message(f"{user.mention} has been warned. Reason: {reason}")

    # Send a message to the channel
    channel = interaction.channel
    if isinstance(channel, nextcord.TextChannel):
        await channel.send(f"{user.mention} has been warned. Reason: {reason}")



"""
This clears certain amount of messages in the server!
"""


@bot.slash_command(description="Deletes a specified number of messages from a channel.")
async def clear(interaction: nextcord.Interaction, number: int):
    """
    Deletes a specified number of messages from a channel.

    Args:
        - number (int): The number of messages to delete.
    """
    # Check if the user has permission to clear messages
    if not interaction.user.guild_permissions.manage_messages:
        return await interaction.response.send_message("You do not have permission to clear messages.")

    # Delete the messages
    deleted = await interaction.channel.purge(limit=number + 1)

    # Send a message indicating the number of messages deleted
    message = f"{len(deleted) - 1} messages have been deleted."
    await interaction.response.send_message(message)









"""
Locks the channel
"""


@bot.slash_command(description="Locks a channel to prevent users from sending messages.")
async def lock(interaction: nextcord.Interaction):
    """
    Locks a channel to prevent users from sending messages.
    """
    # Check if the user has permission to lock the channel
    if not interaction.user.guild_permissions.manage_channels:
        return await interaction.response.send_message("You do not have permission to lock channels.")

    # Lock the channel
    overwrite = nextcord.PermissionOverwrite(send_messages=False)
    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message("This channel has been locked.")






"""
Unlock
"""


@bot.slash_command(description="Unlocks a previously locked channel to allow users to send messages.")
async def unlock(interaction: nextcord.Interaction):
    """
    Unlocks a previously locked channel to allow users to send messages.
    """
    # Check if the user has permission to unlock the channel
    if not interaction.user.guild_permissions.manage_channels:
        return await interaction.response.send_message("You do not have permission to unlock channels.")

    # Unlock the channel
    overwrite = nextcord.PermissionOverwrite(send_messages=True)
    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message("This channel has been unlocked.")








"""
Slowmode 
"""

@bot.slash_command(description="Sets the slowmode delay for a channel.")
async def slowmode(interaction: nextcord.Interaction, duration: int):
    """
    Sets the slowmode delay for a channel.

    Args:
    - duration (int): The duration of the slowmode delay in seconds.
    """
    await interaction.channel.edit(slowmode_delay=duration)
    await interaction.response.send_message(f"Slowmode has been set to {duration} seconds for this channel.")







"""
nickname 
"""


@bot.slash_command(description="Changes the nickname of a user on the server.")
async def nickname(interaction: nextcord.Interaction, user: nextcord.Member, nickname: str):
    """
    Changes the nickname of a user on the server.

    Args:
    - user (nextcord.Member): The member whose nickname should be changed.
    - nickname (str): The new nickname for the user.
    """
    await user.edit(nick=nickname)
    await interaction.response.send_message(f"{user.mention}'s nickname has been changed to {nickname}.")



"""
Role remove or add 
"""


@bot.slash_command(description="Adds or removes a role from a user.")
async def role(interaction: nextcord.Interaction, user: nextcord.Member, action: str, role: nextcord.Role):
    """
    Adds or removes a role from a user.

    Args:
    - user (nextcord.Member): The member whose roles should be modified.
    - action (str): The action to perform - either "add" or "remove".
    - role (nextcord.Role): The role to add or remove.
    """
    if action.lower() == "add":
        await user.add_roles(role)
        await interaction.response.send_message(f"{user.mention} has been given the {role.name} role.")
    elif action.lower() == "remove":
        await user.remove_roles(role)
        await interaction.response.send_message(f"{user.mention} has had the {role.name} role removed.")
    else:
        await interaction.response.send_message("Invalid action. Please specify either 'add' or 'remove'.")












"""
Tempbaan not full 
"""


@bot.slash_command(description="Temporarily bans a user from the server for a specified duration.")
async def tempban(interaction: nextcord.Interaction, user: nextcord.Member, duration: int, reason: str = "No reason provided."):
    """
    Temporarily bans a user from the server for a specified duration.

    Args:
    - user (nextcord.Member): The member to temporarily ban.
    - duration (int): The duration of the ban in seconds.
    - reason (str): The reason for the ban.
    """
    await user.ban(reason=reason, delete_message_days=0)
    await interaction.response.send_message(f"{user.mention} has been temporarily banned for {duration} seconds. Reason: {reason}")
    await asyncio.sleep(duration)
    await user.unban()









"""
Tempmute
"""


@bot.slash_command(description="Temporarily mutes a user in the server for a specified duration.")
async def tempmute(interaction: nextcord.Interaction, user: nextcord.Member, duration: str, reason: str = "No reason provided."):
    """
    Temporarily mutes a user in the server for a specified duration.

    Args:
    - user (nextcord.Member): The member to mute.
    - duration (str): The duration of the mute (e.g. '1h', '2d').
    - reason (str): The reason for the mute.
    """
    duration_seconds = parse_duration(duration)
    await user.edit(mute=True, reason=reason)
    await interaction.response.send_message(f"{user.mention} has been muted for {duration}. Reason: {reason}")
    await asyncio.sleep(duration_seconds)
    await user.edit(mute=False, reason="Mute duration has expired.")
    await interaction.followup.send(f"{user.mention}'s mute duration has expired.")










"""
Strike
"""


@bot.slash_command(description="Issues a strike to a user for breaking server rules.")
async def strike(interaction: nextcord.Interaction, user: nextcord.Member, reason: str):
    """
    Issues a strike to a user for breaking server rules.

    Args:
    - user (nextcord.Member): The member to issue a strike to.
    - reason (str): The reason for issuing the strike.
    """
    strike_channel = nextcord.utils.get(interaction.guild.channels, name="strike-logs")
    if not strike_channel:
        strike_category = await interaction.guild.create_category("Strike Logs")
        strike_channel = await interaction.guild.create_text_channel("strike-logs", category=strike_category)

    strike_count = 1
    strike_message = f"{user.mention} has been given a strike by {interaction.user.mention} for the following reason: {reason}\nTotal Strikes: {strike_count}"

    async for message in strike_channel.history(limit=200):
        if message.author.id == user.id:
            strike_count += 1
            strike_message = f"{user.mention} has been given a strike by {interaction.user.mention} for the following reason: {reason}\nTotal Strikes: {strike_count}"
    
    await strike_channel.send(strike_message)

    try:
        strike_count_message = await user.create_dm()
        await strike_count_message.send(f"You have been given a strike by {interaction.user.mention} for the following reason: {reason}\nTotal Strikes: {strike_count}")
    except:
        pass











"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""


@bot.slash_command(description="Track when a user creates an invite to the server")
async def invitetracker(interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):
    """
    Track when a user creates an invite to the server.
    """
    invites = await interaction.guild.invites()
    num_invites = len(invites)

    async def on_invite_create(invite):
        nonlocal num_invites
        num_invites += 1
        embed = nextcord.Embed(title="New Invite Created", description=f"{invite.inviter} created invite {invite.code}. Total invites: {num_invites}", color=0x00ff00)
        if channel:
            await channel.send(embed=embed)
        else:
            await interaction.response.send_message(embed=embed)

    bot.add_listener(on_invite_create, name='on_invite_create')

    if channel:
        embed = nextcord.Embed(title="Invite Tracker Started", description=f"Alert messages will be sent to {channel.mention}. Total invites: {num_invites}", color=0x00ff00)
        await interaction.response.send_message(embed=embed)
    else:
        embed = nextcord.Embed(title="Invite Tracker Started", description=f"Total invites: {num_invites}", color=0x00ff00)
        await interaction.response.send_message(embed=embed)

 






"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""


# BAN COMMAND 
@bot.slash_command(description="Ban a user from the server.")
async def ban(interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided."):
    """
    Ban a user from the server.

    Args:
    - user (nextcord.Member): The member to ban.
    - reason (str): The reason for the ban.
    """
    await user.ban(reason=reason)
    await interaction.response.send_message(f"{user.mention} has been banned. Reason: {reason}")







"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""


@bot.slash_command(description="Kick a user from the server.")
async def kick(interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided."):
    """
    Kick a user from the server.

    Args:
    - user (nextcord.Member): The member to kick.
    - reason (str): The reason for the kick.
    """
    await user.kick(reason=reason)
    await interaction.response.send_message(f"{user.mention} has been kicked. Reason: {reason}")






"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command(description="Unban a user from the server.")
async def unban(interaction: nextcord.Interaction, user: nextcord.User, reason: str = "No reason provided."):
    """
    Unban a user from the server.

    Args:
    - user (nextcord.User): The user to unban.
    - reason (str): The reason for the unban.
    """
    await interaction.guild.unban(user, reason=reason)
    await interaction.response.send_message(f"{user.mention} has been unbanned. Reason: {reason}")








"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

# Mute a user in the server
@bot.slash_command(description="Mute a user in the server.")
async def mute(interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided."):
    """
    Mute a user in the server.

    Args:
    - user (nextcord.Member): The member to mute.
    - reason (str): The reason for the mute.
    """
    role = nextcord.utils.get(interaction.guild.roles, name="Muted")
    await user.add_roles(role, reason=reason)
    await interaction.response.send_message(f"{user.mention} has been muted. Reason: {reason}")









"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""


# Unmute a user in the server
@bot.slash_command(description="Unmute a user in the server.")
async def unmute(interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided."):
    """
    Unmute a user in the server.

    Args:
    - user (nextcord.Member): The member to unmute.
    - reason (str): The reason for the unmute.
    """
    role = nextcord.utils.get(interaction.guild.roles, name="Muted")
    await user.remove_roles(role, reason=reason)
    await interaction.response.send_message(f"{user.mention} has been unmuted. Reason: {reason}")










"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

# Add a role to a user in the server
@bot.slash_command(description="Add a role to a user in the server.")
async def add_role(interaction: nextcord.Interaction, user: nextcord.Member, role: nextcord.Role, reason: str = "No reason provided."):
    """
    Add a role to a user in the server.

    Args:
    - user (nextcord.Member): The member to add the role to.
    - role (nextcord.Role): The role to add.
    - reason (str): The reason for adding the role.
    """
    await user.add_roles(role, reason=reason)
    await interaction.response.send_message(f"{role.mention} has been added to {user.mention}. Reason: {reason}")
    
    








"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

    # removes role from user
@bot.slash_command(description="Remove a role from a user in the server.")
async def remove_role(interaction: nextcord.Interaction, user: nextcord.Member, role: nextcord.Role, reason: str = "No reason provided."):
    """
    Remove a role from a user in the server.

    Args:
    - user (nextcord.Member): The member to remove the role from.
    - role (nextcord.Role): The role to remove.
    - reason (str): The reason for removing the role.
    """
    await user.remove_roles(role, reason=reason)
    await interaction.response.send_message(f"{role.mention} has been removed from {user.mention}. Reason: {reason}")











"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command(description="Mute a user in a voice channel.")
async def mutevoice(interaction: nextcord.Interaction, member: nextcord.Member, reason: str = "No reason provided."):
    """
    Mute a user in a voice channel.

    Args:
    - member (nextcord.Member): The member to mute.
    - reason (str): The reason for muting the user.
    """
    await member.edit(mute=True, reason=reason)
    await interaction.response.send_message(f"{member.mention} has been muted in the voice channel. Reason: {reason}")








"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""


@bot.slash_command(description="Unmute a user in a voice channel.")
async def unmutevoice(interaction: nextcord.Interaction, member: nextcord.Member, reason: str = "No reason provided."):
    """
    Unmute a user in a voice channel.

    Args:
    - member (nextcord.Member): The member to unmute.
    - reason (str): The reason for unmuting the user.
    """
    await member.edit(mute=False, reason=reason)
    await interaction.response.send_message(f"{member.mention} has been unmuted in the voice channel. Reason: {reason}")









"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""


@bot.slash_command(description="Deafen a user in a voice channel.")
async def deafen(interaction: nextcord.Interaction, member: nextcord.Member, reason: str = "No reason provided."):
    """
    Deafen a user in a voice channel.

    Args:
    - member (nextcord.Member): The member to deafen.
    - reason (str): The reason for deafening the user.
    """
    await member.edit(deafen=True, reason=reason)
    await interaction.response.send_message(f"{member.mention} has been deafened in the voice channel. Reason: {reason}")








"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""


@bot.slash_command(description="Undeafen a user in a voice channel.")
async def undeafen(interaction: nextcord.Interaction, member: nextcord.Member, reason: str = "No reason provided."):
    """
    Undeafen a user in a voice channel.

    Args:
    - member (nextcord.Member): The member to undeafen.
    - reason (str): The reason for undeafening the user.
    """
    await member.edit(deafen=False, reason=reason)
    await interaction.response.send_message(f"{member.mention} has been undeafened in the voice channel. Reason: {reason}")









"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""


@bot.slash_command(description="Send a customized announcement.")
async def announce(
    interaction: nextcord.Interaction,
    title: str,
    message: str,
    channel: nextcord.TextChannel,
    mention: bool = False
):
    """
    Send a customized announcement in the specified channel.

    Args:
    - title (str): The title of the announcement.
    - message (str): The message to be included in the announcement.
    - channel (nextcord.TextChannel): The channel to send the announcement in.
    - mention (bool): Whether or not to mention the @everyone role in the announcement. Defaults to False.
    """
    # Create the announcement embed
    embed = nextcord.Embed(
        title=title,
        description=message,
        color=0xff0000
    )
    
    # Mention @everyone if requested
    if mention:
        content = "@everyone"
    else:
        content = None
    
    # Send the announcement message
    await channel.send(content=content, embed=embed)
    
    # Send a response to the user
    await interaction.response.send_message(f"Announcement sent in {channel.mention}!")









"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

@bot.slash_command(description="Set a reminder message to repeat in a set amount of hours.")
async def remind2(
    interaction: nextcord.Interaction,
    title: str,
    message: str,
    channel: nextcord.TextChannel,
    repeat_hours: int,
    mention: bool = False
):
    """
    Set a reminder message to repeat in a set amount of hours.

    Args:
    - title (str): The title of the reminder message.
    - message (str): The message to be included in the reminder.
    - channel (nextcord.TextChannel): The channel to send the reminder in.
    - repeat_hours (int): The number of hours to wait before repeating the reminder message.
    - mention (bool): Whether or not to mention the @everyone role in the reminder message. Defaults to False.
    """
    # Create the reminder embed
    embed = nextcord.Embed(
        title=title,
        description=message,
        color=0xff0000
    )
    
    # Mention @everyone if requested
    if mention:
        content = "@everyone"
    else:
        content = None
    
    # Send the initial reminder message
    reminder_msg = await channel.send(content=content, embed=embed)
    
    # Send a response to the user
    await interaction.response.send_message(f"Reminder set for {repeat_hours} hours in {channel.mention}!")
    
    # Define a function to repeat the reminder message
    async def repeat_reminder():
        await asyncio.sleep(repeat_hours * 3600) # Wait for the set number of hours
        while True:
            # Send the reminder message
            reminder_msg = await channel.send(content=content, embed=embed)
            await asyncio.sleep(repeat_hours * 3600) # Wait for the set number of hours again
    
    # Start the repeating reminder loop as a background task
    bot.loop.create_task(repeat_reminder())







"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""


@bot.slash_command(description="Make the bot talk in a channel.")
async def talk2(
    interaction: nextcord.Interaction,
    channel: nextcord.TextChannel,
    message: str
):
    """
    Make the bot talk in a channel.

    Args:
    - channel (nextcord.TextChannel): The channel to send the message in.
    - message (str): The message to be sent in the channel.
    """
    # Send the message to the specified channel
    await channel.send(message)

    # Send a response to the user
    await interaction.response.send_message(f"Message sent to {channel.mention}!")



"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""


# Award points to user
@bot.event
async def on_message(message):
    # Ignore messages from bots
    if message.author.bot:
        return
    
    # Increment user points
    user_id = str(message.author.id)
    user_points[user_id] = user_points.get(user_id, 0) + 1
    
    # Check user's point rank
    points_needed = [1000, 2500, 5000, 10000, 25000, 50000, 100000, 250000]
    rank = 0
    for points in points_needed:
        if user_points[user_id] < points:
            break
        rank += 1
    
    # Send message if user has ranked up
    if rank > 0 and rank <= len(points_needed):
        await message.channel.send(f"{message.author.mention} has ranked up to rank {rank}! 🎉")
    
    # Pass the message to other event handlers
    await bot.process_commands(message)


"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# Command to check user's points
@bot.command()
async def points2(ctx):
    user_id = str(ctx.author.id)
    points = user_points.get(user_id, 0)
    await ctx.send(f"{ctx.author.mention} has {points} points!")




@bot.event
async def on_member_join(member):
    # Get the server's welcome channel
    welcome_channel = nextcord.utils.get(member.guild.text_channels, name="welcome")
    if welcome_channel is None:
        return
    
    # Create the welcome message
    embed = nextcord.Embed(
        title=f"Welcome {member.display_name}!",
        description="Thanks for joining the server.",
        color=0x00ff00
    )
    
    avatar = member.display_avatar
    embed = nextcord.Embed(title=f"Welcome {member.name} to the {member.guild.name} Community! We hope you enjoy your stay!", color=0x0000ff)
    embed.set_image(url=avatar)
    embed.add_field(name="ℹ️ Information", value="Please read the rules in the #rules channel!")
    embed.set_footer(text="Bot by wade#1781")
    
    # Send the welcome message to the welcome channel
    await welcome_channel.send(embed=embed)







"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# Listen for the "on_guild_join" event
@bot.event
async def on_guild_join(guild):
    # Set up the suggestion channel and log channel
    suggestion_channel, suggestion_log_channel = await setup(guild)
    print(f'Successfully set up suggestion channels in {guild.name} ({guild.id})')

# Command to submit a suggestion
@bot.slash_command(description='Submit a suggestion.')
async def suggest4(interaction: nextcord.Interaction, suggestion: str):
    # Get the suggestion channel and log channel
    guild = interaction.guild
    suggestion_channel = nextcord.utils.get(guild.text_channels, name='suggestions')
    suggestion_log_channel = nextcord.utils.get(guild.text_channels, name='suggestion-log')

    # Check if suggestion channel and log channel exist
    if not suggestion_channel or not suggestion_log_channel:
        # If either channel is missing, set up both channels
        suggestion_channel, suggestion_log_channel = await setup(guild)

     # Send the suggestion to the suggestion channel
    suggestion_embed = nextcord.Embed(title='New Suggestion', description=suggestion)
    suggestion_embed.set_footer(text=f"Suggested by {interaction.user.name}#{interaction.user.discriminator}")
    suggestion_msg = await suggestion_channel.send(embed=suggestion_embed)

    # Send a response to the user
    await interaction.response.send_message(f'Thanks for your suggestion! It has been submitted to {suggestion_channel.mention}.')

    # Send a message to the suggestion log channel
    suggestion_log_embed = nextcord.Embed(title='New Suggestion', description=suggestion)
    suggestion_log_embed.add_field(name='Suggestion ID', value=suggestion_msg.id)
    suggestion_log_embed.add_field(name='Suggested by', value=interaction.user.mention)
    suggestion_log_embed.add_field(name='Suggestion channel', value=suggestion_channel.mention)
    await suggestion_log_channel.send(embed=suggestion_log_embed)
    
"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command(description='Return the input text as a code block.')
async def codeblock(interaction: nextcord.Interaction, text: str):
    codeblock_text = f'```{text}```'
    await interaction.response.send_message(codeblock_text)


"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

@bot.slash_command(description='Format text as a quote.')
async def quotetext(interaction: nextcord.Interaction, text: str):
    """
    Format text as a quote.

    Args:
    - text (str): The text to format as a quote.
    """
    # Create the quote block
    quote_block = f'```\n{text}\n```'

    # Send the quote block as a message
    await interaction.response.send_message(quote_block)
    
    

"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command(description='Encode a message in Base64.')
async def encodebase64(interaction: nextcord.Interaction, message: str):
    # Encode the message in Base64
    encoded_message = base64.b64encode(message.encode('utf-8')).decode('utf-8')

    # Send the encoded message as a code block
    await interaction.response.send_message(f'```\n{encoded_message}\n```')
    
    
"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""  
@bot.slash_command(description='Generate a random password.')
async def generatepassword(interaction: nextcord.Interaction, length: int = 16):
    # Generate a random password of the specified length
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    # Send the password as a code block
    await interaction.response.send_message(f'```\n{password}\n```')   
    
"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
    
@bot.slash_command(description='Reverse a message.')
async def reverse(interaction: nextcord.Interaction, message: str):
    # Reverse the message
    reversed_message = message[::-1]

    # Send the reversed message as a code block
    await interaction.response.send_message(f'```\n{reversed_message}\n```')

"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

@bot.slash_command(description='Count the number of words in a message.')
async def word_count(interaction: nextcord.Interaction, message: str):
    # Count the number of words in the message
    word_count = len(message.split())

    # Send the word count as a code block
    await interaction.response.send_message(f'```\n{word_count}\n```')



"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command(description='Encrypt text using the Caesar cipher.')
async def encrypt_caesar(
    interaction: nextcord.Interaction,
    text: str,
    shift: int
):
    # Convert text to uppercase
    text = text.upper()

    # Define alphabets for encryption
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]

    # Encrypt the text using the Caesar cipher
    encrypted_text = ''
    for char in text:
        if char in alphabet:
            encrypted_text += shifted_alphabet[alphabet.index(char)]
        else:
            encrypted_text += char

    # Send the encrypted text to the user
    await interaction.response.send_message(f'Encrypted text: `{encrypted_text}`')
    
    
"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""   

@bot.slash_command(description='Calculate the sum of two numbers.')
async def add(interaction: nextcord.Interaction, num1: int, num2: int):
    """
    Calculate the sum of two numbers.

    Args:
    - num1 (int): The first number.
    - num2 (int): The second number.
    """
    # Calculate the sum of the two numbers
    result = num1 + num2

    # Send the result as a message
    await interaction.response.send_message(f'The sum of {num1} and {num2} is {result}.')



"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

@bot.slash_command(description='Get a random Chuck Norris joke.')
async def chucknorris(interaction: nextcord.Interaction):
    """
    Get a random Chuck Norris joke.
    """
    # Fetch a random Chuck Norris joke from the API
    response = requests.get('https://api.chucknorris.io/jokes/random')

    # Extract the joke text from the response JSON
    joke = response.json()['value']

    # Send the joke as a message
    await interaction.response.send_message(joke)

"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

@bot.slash_command(description='Get a random dad joke.')
async def dadjoke(interaction: nextcord.Interaction):
    """
    Get a random dad joke.
    """
    # Fetch a random dad joke from the API
    response = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'text/plain'})

    # Extract the joke text from the response
    joke = response.text

    # Send the joke as a message
    await interaction.response.send_message(joke)

"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

@bot.slash_command(description='Get the definition of a word from the Merriam-Webster dictionary.')
async def define(interaction: nextcord.Interaction, word: str):
    """
    Get the definition of a word from the Merriam-Webster dictionary.

    Args:
    - word (str): The word to define.
    """
    # Fetch the definition of the word from the API
    response = requests.get(f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key=YOUR_API_KEY_HERE')

    # Extract the first definition from the response JSON
    data = response.json()
    definition = data[0]['shortdef'][0]

    # Send the definition as a message
    await interaction.response.send_message(f'The definition of {word} is: {definition}.')

"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

@bot.slash_command(description='Get a random programming joke.')
async def progjoke(interaction: nextcord.Interaction):
    """
    Get a random programming joke.
    """
    # Fetch a random programming joke from the API
    response = requests.get('https://official-joke-api.appspot.com/jokes/programming/random')

    # Extract the joke setup and punchline from the response JSON
    data = response.json()[0]
    setup = data['setup']
    punchline = data['punchline']

    # Send the joke as a message
    await interaction.response.send_message(f'{setup}\n{punchline}')

"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command(description='Get a random trivia question.')
async def trivia(interaction: nextcord.Interaction):
    """
    Get a random trivia question.
    """
    # Fetch a random trivia question from the API
    response = requests.get('https://opentdb.com/api.php?amount=1')

    # Extract the question and answer choices from the response JSON
    data = response.json()['results'][0]
    question = data['question']
    choices = data['incorrect_answers'] + [data['correct_answer']]
    random.shuffle(choices)

    # Format the answer choices as a string
    choices_str = '\n'.join(choices)

    # Send the question and answer choices as a message
    await interaction.response.send_message(f'{question}\n\n{choices_str}')




"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command(description='Get the lyrics of a song.')
async def lyrics(interaction: nextcord.Interaction, artist: str, song: str):
    """
    Get the lyrics of a song.

    Args:
    - artist (str): The artist of the song.
    - song (str): The title of the song.
    """
    # Fetch the lyrics of the song from the API
    response = requests.get(f'https://api.lyrics.ovh/v1/{artist}/{song}')

    # Extract the lyrics from the response JSON
    data = response.json()
    lyrics = data['lyrics']

    # Send the lyrics as a message
    await interaction.response.send_message(lyrics)


"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command(description='Calculate the average of a list of numbers.')
async def calculate_average(interaction: nextcord.Interaction, numbers: str):
    """
    Calculate the average of a list of numbers.

    Args:
    - numbers (str): A comma-separated list of numbers.
    """
    # Convert the comma-separated string of numbers to a list of floats
    numbers_list = [float(n) for n in numbers.split(',')]

    # Calculate the average of the numbers
    average = sum(numbers_list) / len(numbers_list)

    # Send the calculated average as a message
    await interaction.response.send_message(f'Average: {average}')



"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
wiki = wikipediaapi.Wikipedia('en')

@bot.slash_command(
    name='wiki',
    description='Retrieve a summary of a given topic from Wikipedia.'
)
async def wiki_summary(interaction: nextcord.Interaction, topic: str):
    """
    Retrieve a summary of a given topic from Wikipedia.

    Args:
    - topic (str): The topic to retrieve a summary for.
    """
    # Retrieve the summary for the given topic from Wikipedia
    page = wiki.page(topic)
    if page.exists():
        summary = page.summary
    else:
        summary = f'Unable to retrieve a summary for "{topic}" at this time.'

    # Split the summary into chunks of 2000 characters or less
    chunks = [summary[i:i+2000] for i in range(0, len(summary), 2000)]

    # Send each chunk as a separate message
    for chunk in chunks:
        await interaction.response.send_message(chunk)
    
"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""    
@bot.slash_command(
    name='celsius',
    description='Convert a temperature from Celsius to Fahrenheit.'
)
async def celsius_to_fahrenheit(interaction: nextcord.Interaction, celsius: float):
    """
    Convert a temperature from Celsius to Fahrenheit.

    Args:
    - celsius (float): The temperature in Celsius to convert.
    """
    # Convert the temperature from Celsius to Fahrenheit
    fahrenheit = (celsius * 9/5) + 32

    # Send the converted temperature as a message
    message = f'{celsius} degrees Celsius is equal to {fahrenheit} degrees Fahrenheit.'
    await interaction.response.send_message(message)    
    
"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""    
@bot.slash_command(
    name='advertise',
    description='Advertise the bot and its features.'
)
async def advertise_bot(interaction: nextcord.Interaction):
    """
    Advertise the bot and its features.
    """
    # Create a message with information about the bot and its features
    message = """
    **Welcome to Wadder!**
    
    Wadder is a powerful and easy-to-use bot that can help you with a wide range of tasks. Here are some of its key features:
    
    - Slash commands for easy access to bot functionality
    - Customizable settings and preferences
    - Integration with third-party APIs for additional functionality
    - Moderation tools to help keep your server safe and secure
    - And much more!
    
    To get started with Wadder, simply invite it to your server and type `/help` to see a list of available commands.
    """

    # Send the advertisement message as a message
    await interaction.response.send_message(message)    
    
    
"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""    
@bot.slash_command(
    name='advertise2',
    description='Advertise your server in a linked channel.'
)
async def advertise_server(interaction: nextcord.Interaction, message: str):
    """
    Advertise the user's server in a linked channel.

    Args:
    - message (str): The advertisement message to send to the linked channel.
    """
    # Check if the user has permission to use this command
    if not interaction.channel.permissions_for(interaction.user).administrator:
        return await interaction.response.send_message('You must be an administrator to use this command.')

    # Retrieve the main server and the advertisement channel
    main_server = bot.get_guild(850958118049677312)
    ad_channel = main_server.get_channel(1024442696527523891) # change to avd channel 

      # Create the invite link with server icon and join button
    invite_link = await interaction.channel.create_invite(
        max_age=0,
        max_uses=0,
        unique=True,
        reason='Server advertisement invite'
    )
    invite_embed = nextcord.Embed(
        title='Join Our Server!',
        url=invite_link.url,
        description=f'Click the "Join" button below to join our server!\n{message}',
        color=nextcord.Color.blurple()
    )
    invite_embed.set_thumbnail(url=interaction.guild.icon.url)
    invite_embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
    invite_embed.set_footer(text='Server Advertisement Invite')

    # Send the advertisement message and the invite link to the advertisement channel
    await ad_channel.send(embed=invite_embed)

    # Send a confirmation message to the user
    await interaction.response.send_message('Your advertisement has been sent to the linked channel.')

"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""    
@bot.command()
async def game_deals(ctx):
    """
    Sends a notification to the specified channel with details about any free or discounted games on Steam.
    """
    while True:
        # Make a GET request to the Steam API to get a list of current specials
        url = "https://store.steampowered.com/api/featuredcategories"
        params = {
            "cc": "US",
            "l": "en",
            "v": 1,
            "tag": "specials"
        }
        response = requests.get(url, params=params)

        # Parse the JSON response to get a list of games on sale or for free
        data = response.json()
        specials = data["specials"]["items"]

        # Create a message to send to the notification channel
        message = "New game deals available on Steam:\n"
        for game in specials:
            if game["discount_percent"] > 0:
                discount_price = game.get("discount_final_price_formatted", "Unknown")
                message += f"{game['name']} - {game['discount_percent']}% off ({discount_price})\n"
            else:
                message += f"{game['name']} - free to play!\n"

        # Send the message to the notification channel
        channel = bot.get_channel(1072295747686506499)
        await channel.send(message)

        # Send a confirmation message to the command author
        await ctx.send("Game deals notification sent!")
        
        # Wait for 6 hours before sending the next update
        await asyncio.sleep(6 * 60 * 60)



"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""    
@bot.slash_command(
    name="game_deals2",
    description="Sends a notification with details about any free or discounted games on Steam."
)
async def send_game_deals(ctx, channel: nextcord.TextChannel):
    """
    Sends a notification to the specified channel with details about any free or discounted games on Steam.
    """
    while True:
        # Make a GET request to the Steam API to get a list of current specials
        url = "https://store.steampowered.com/api/featuredcategories"
        params = {
            "cc": "US",
            "l": "en",
            "v": 1,
            "tag": "specials"
        }
        response = requests.get(url, params=params)

        # Parse the JSON response to get a list of games on sale or for free
        data = response.json()
        specials = data["specials"]["items"]

        # Create an embed to send to the notification channel
        embed = nextcord.Embed(title="New game deals available on Steam:", color=0x00ff00)
        for game in specials:
            if game["discount_percent"] > 0:
                discount_price = game.get("discount_final_price_formatted")
                embed.add_field(name=f"{game['name']} - {game['discount_percent']}% off",
                                value=f"{discount_price}", inline=False)
            else:
                embed.add_field(name=f"{game['name']} - free to play!", value="\u200b", inline=False)

        # Send the embed to the specified notification channel and delete the previous message if it exists
        if hasattr(send_game_deals, "last_message"):
            await send_game_deals.last_message.delete()
        send_game_deals.last_message = await channel.send(embed=embed)

        # Send a confirmation message to the command author
        await ctx.send(f"Game deals notification sent to {channel.mention}!")

        # Wait for 24 hours before checking for updates again
        await asyncio.sleep(24 * 60 * 60)
        
openai_model_engine = "text-davinci-003" # You can change this to another OpenAI model engine if you'd like        


"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# example; !translate2 en fr hello world zh: Chinese
#es: Spanish
#fr: French
#de: German
#ja: Japanese
#pt: Portuguese
#it: Italian
#ar: Arabic
#ru: Russian
#ko: Korean
#tr: Turkish
#nl: Dutch
#pl: Polish
#sv: Swedish
#da: Danish
#fi: Finnish
#no: Norwegian
#el: Greek
#hi: Hindi
#he: Hebrew
#id: Indonesian
#th: Thai
#cs: Czech
#ro: Romanian
#vi: Vietnamese
#sr: Serbian
#sk: Slovak
#hr: Croatian
#bn: Bengali
#hu: Hungarian
#fil: Filipino
#uk: Ukrainian
#fa: Persian
#ms: Malay
#sl: Slovenian
@bot.slash_command()
async def translate2(interaction: nextcord.Interaction, source_language: str, target_language: str, text: str):
    """
    Translates text from one language to another using OpenAI.
    Usage: /translate2 <source_language> <target_language> <text to translate>
    """
    # Call the OpenAI API to translate the text
    completions = openai.Completion.create(
        engine=openai_model_engine,
        prompt=f"Translate from {source_language} to {target_language}: {text}",
        max_tokens=64,
        n=1,
        stop=None,
        temperature=0.5,
    )
    translated_text = completions.choices[0].text.strip()

    # Send the translated text back to the user
    await interaction.response.send_message(f"{translated_text}")  


"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

@bot.slash_command()
async def summarize(interaction: nextcord.Interaction, text: str):
    """
    Summarize text using the Davinci 003 engine.
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Please summarize the following text:\n{text}\nSummary:",
        max_tokens=60,
        temperature=0.7,
    )
    summary = response.choices[0].text.strip()
    await interaction.response.send_message(f"Here's a summary of the text:\n{summary}")

"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command()
async def generate_code2(interaction: nextcord.Interaction):
    """
    Generate code snippets using the Davinci 003 engine.
    """
    await interaction.response.defer()
    await interaction.followup.send("What's the problem description?", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    code_description = response.content
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{code_description}\nCode:",
        max_tokens=1024,
        temperature=0.7,
    )
    code_snippet = response.choices[0].text.strip()
    await interaction.followup.send(f"Here's some code that solves the problem:\n```{code_snippet}```")
"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""        
@bot.slash_command()
async def generate_poem(interaction: nextcord.Interaction):
    """
    Generate a poem using the Davinci 003 engine.
    """
    await interaction.response.defer()
    await interaction.followup.send("What's the poem prompt?", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    prompt = response.content
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Write a poem based on the following prompt:\n{prompt}\nPoem:",
        max_tokens=1024,
        temperature=0.7,
    )
    poem = response.choices[0].text.strip()
    await interaction.followup.send(f"Here's your poem:\n```{poem}```")

"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command()
async def generate_story(interaction: nextcord.Interaction):
    """
    Generate a short story using the Davinci 003 engine.
    """
    await interaction.response.defer()
    await interaction.followup.send("What's the story prompt?", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    prompt = response.content
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Write a short story based on the following prompt:\n{prompt}\nStory:",
        max_tokens=1024,
        temperature=0.7,
    )
    story = response.choices[0].text.strip()
    await interaction.followup.send(f"Here's your story:\n```{story}```")

"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command()
async def generate_lyrics(interaction: nextcord.Interaction):
    """
    Generate song lyrics using the Davinci 003 engine.
    """
    await interaction.response.defer()
    await interaction.followup.send("What's the song prompt?", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    prompt = response.content
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Write lyrics for a song based on the following prompt:\n{prompt}\nLyrics:",
        max_tokens=1024,
        temperature=0.7,
    )
    lyrics = response.choices[0].text.strip()
    await interaction.followup.send(f"Here are your lyrics:\n```{lyrics}```")

"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command()
async def generate_product_name(interaction: nextcord.Interaction):
    """
    Generate a unique product name using the Davinci 003 engine.
    """
    await interaction.response.defer()
    await interaction.followup.send("What's the product prompt?", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    prompt = response.content
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate a unique product name based on the following prompt:\n{prompt}\nProduct name:",
        max_tokens=1024,
        temperature=0.7,
    )
    product_name = response.choices[0].text.strip()
    await interaction.followup.send(f"Here's your product name:\n```{product_name}```")
    


"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""

@bot.slash_command()
async def generate_images(interaction: nextcord.Interaction):
    """
    Generate images using the Dall-E 2 engine.
    """
    await interaction.response.defer()
    await interaction.followup.send("What do you want to generate an image of?", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    prompt = response.content
    await interaction.followup.send("How many images do you want to generate?", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    n = int(response.content)
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size="1024x1024"
    )
    images = response['data']
    for image in images:
        with io.BytesIO() as image_binary:
            # Download the image data and write it to a BytesIO buffer
            response = requests.get(image['url'])
            image_binary.write(response.content)
            # Reset the buffer position to the beginning
            image_binary.seek(0)
            # Send the image file to the Discord channel
            await interaction.followup.send(file=nextcord.File(image_binary, filename='generated_image.png'))














    
    
    
    
    
    
    
    
    
"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""  
    
    
@bot.slash_command()
async def generate_financial_advice(interaction: nextcord.Interaction):
    """
    Generate personalized financial advice using the Davinci 003 engine. This is for fun not to be used for real life!
    """
    await interaction.response.defer()
    await interaction.followup.send("Please provide your financial data:", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    financial_data = response.content
    
    # Generate financial advice using OpenAI's API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Given the following financial data:\n{financial_data}\nProvide personalized financial advice:",
        max_tokens=1024,
        temperature=0.7,
    )
    advice = response.choices[0].text.strip()
    
    # Send the financial advice in a nice embed
    embed = nextcord.Embed(
        title="Personalized Financial Advice",
        description=advice,
        color=nextcord.Color.blue()
    )
    embed.set_footer(text="This advice is for fun and should not be taken as professional financial advice.")
    await interaction.followup.send(embed=embed) 







"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command()
async def generate_program(interaction: nextcord.Interaction):
    """
    Generate a complex software program using the Davinci 003 engine.
    """
    await interaction.response.defer()
    await interaction.followup.send("Please provide your program requirements:", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    program_requirements = response.content
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Given the following program requirements:\n{program_requirements}\nProvide a complex software program:",
        max_tokens=1024,
        temperature=0.7,
    )
    program = response.choices[0].text.strip()
    await interaction.followup.send(embed=nextcord.Embed(title="Generated Program", description=program))  #make a code snippet 
    









"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""    
@bot.slash_command()
async def generate_legal_document(interaction: nextcord.Interaction):
    """
    Generate legal documents using the Davinci 003 engine. Not true legal advice!
    """
    await interaction.response.defer()
    await interaction.followup.send("Please provide the necessary information for the legal document:", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    legal_info = response.content
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Given the following legal information:\n{legal_info}\nGenerate the legal document:",
        max_tokens=2048,
        temperature=0.7,
    )
    document = response.choices[0].text.strip()
    embed = nextcord.Embed(title="Generated Legal Document", description=document, color=0x00ff00)
    await interaction.followup.send(embed=embed)    
    






"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
# needs more formating 

@bot.slash_command()
async def poll(interaction: nextcord.Interaction, time: int, title: str, options: str):
    """
    Example: /poll 30 "Favorite Color" "Red|Green|Blue"
    """

    # Check if required parameters are missing
    if not all((time, title, options)):
        await interaction.response.send_message("Please specify the time, title, and options!", ephemeral=True)
        return

    # Parse options from input string
    options = options.split('|')

    # Check if too many options were provided
    MAX_OPTIONS = 6
    if len(options) > MAX_OPTIONS:
        await interaction.response.send_message(f"Maximum number of options is {MAX_OPTIONS}!", ephemeral=True)
        return

    # Calculate poll end time
    end_time = datetime.now() + timedelta(minutes=time)
    formatted_end_time = nextcord.utils.format_dt(end_time, style="T")

    # Create and send embed with poll options
    options_text = "\n".join([f"`{i}.` {option}" for i, option in enumerate(options, start=1)])

    # Define the color for the embed
    EMBED_COLOR = 0x3498db

    embed = nextcord.Embed(color=EMBED_COLOR, title=title)
    embed.add_field(name="Options", value=options_text, inline=False)
    embed.set_footer(text=f"Poll ends at {formatted_end_time}")

    poll_message = await interaction.channel.send(embed=embed)

    # Add reactions to poll message
    for i in range(1, len(options) + 1):
        await poll_message.add_reaction(f"{i}\uFE0F\u20E3")

    # Send confirmation message to user
    await interaction.response.send_message(f"Poll created in {interaction.channel.mention}!", ephemeral=True)

















"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command(name="edit", description="Fix spelling mistakes in a message")
async def edit(interaction: nextcord.Interaction, text: str):
    # Use the OpenAI API to edit the text
    response = openai.Edit.create(model="text-davinci-edit-001", input=text, instruction="Fix the spelling mistakes")
    edited_text = response["choices"][0]["text"]
    
    # Send the edited text as a reply to the user's interaction
    await interaction.response.send_message(f"{interaction.user.mention} said: {edited_text}", ephemeral=True)












"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""
@bot.slash_command()
async def generate_technical_documentation(interaction: nextcord.Interaction):
    """
    Generate technical documentation using the Davinci 003 engine.
    """
    await interaction.response.defer()
    await interaction.followup.send("Please provide the name of the software program or system:", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    software_name = response.content
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate technical documentation for the {software_name} software program or system:",
        max_tokens=2048,
        temperature=0.7,
    )
    document = response.choices[0].text.strip()
    embed = nextcord.Embed(title="Generated Technical Documentation", description=document, color=0x00ff00)
    await interaction.followup.send(embed=embed)

###########################################





"""
This is the start of the bot  (on ready)
Prettiest I can get it. 
"""







# works but very much wip! (have to use the actually name for the role)

@bot.slash_command()
async def verifyrules2(interaction: nextcord.Interaction):
    def check(reaction, user):
        return user == interaction.user and str(reaction.emoji) == '✅'

    # Create the embed for the rules
    rules_embed = nextcord.Embed(title="Server Rules", description="Please read and follow the rules below:")

    # Prompt the user to input the rules one by one
    await interaction.response.send_message('Please input the rules one by one. Type "quit" to finish:')
    rules = []
    while True:
        rule = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
        if rule.content.lower() == 'quit':
            break
        rules.append(rule.content)

    # Add the rules to the embed
    for i, rule in enumerate(rules):
        rules_embed.add_field(name=f"Rule {i+1}", value=rule, inline=False)

    # Prompt the user to specify the channel to send the rules to
    await interaction.followup.send('Please specify the channel to send the rules to (mention the channel):')
    channel_input = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    channel = nextcord.utils.get(interaction.guild.channels, mention=channel_input.content)

    # Prompt the user to specify the role to assign to verified users
    await interaction.followup.send('Please specify the role to assign to verified users:')
    role_input = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    role_name = role_input.content
    print(f'Role name: {role_name}')
    role = nextcord.utils.get(interaction.guild.roles, name=role_name)
    print(f'Role: {role}')

    # Send the rules as an embed to the specified channel
    rules_message = await channel.send(embed=rules_embed)

    # Add the verification check mark
    await rules_message.add_reaction('✅')
    await interaction.followup.send(f'The rules have been sent to {channel.mention}. React with ✅ on the rules message to gain access to other areas of the Discord server.')

    # Wait for the user to react to the rules message
    reaction, user = await bot.wait_for('reaction_add', check=check)
    await user.add_roles(role)
    await interaction.followup.send(f'{user.mention} has been verified and now has access to other areas of the server.')







@bot.slash_command()
async def countdown(interaction: nextcord.Interaction, event_name: str):
    """Countdown to a specified event."""
    await interaction.response.defer()

    await interaction.followup.send(f"What's the date and time of the {event_name}? (Please use the following format: YYYY-MM-DD HH:MM)", ephemeral=True)

    def check(m):
        return m.author == interaction.user

    try:
        event_datetime = await bot.wait_for('message', check=check, timeout=30.0)
        event_datetime = event_datetime.content.strip()
        event_datetime = parser.parse(event_datetime)
    except nextcord.NotFound:
        await interaction.followup.send("Sorry, I couldn't find your response. Please try again.", ephemeral=True)
        return
    except asyncio.TimeoutError:
        await interaction.followup.send("Sorry, you didn't respond in time. Please try again.", ephemeral=True)
        return
    except ValueError:
        await interaction.followup.send("Sorry, that's not a valid date and time. Please try again.", ephemeral=True)
        return

    now = datetime.utcnow()
    time_diff = event_datetime - now

    days, seconds = time_diff.days, time_diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    countdown = f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds until {event_name}!"

    await interaction.followup.send(countdown, ephemeral=True)


















@bot.slash_command()
async def send_news(interaction: nextcord.Interaction):
    """Send news updates to a specified channel."""
    await interaction.response.defer()
    await interaction.followup.send("Please provide the channel where the news updates should be sent:", ephemeral=True)
    response = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
    channel = response.channel_mentions[0]
    
    await interaction.followup.send("Sending news updates to " + channel.mention, ephemeral=True)
    
    feed = feedparser.parse("http://rss.cnn.com/rss/edition.rss")
    index = 0

    while True:
        post = feed.entries[index]
        await channel.send(post.title + ": " + post.link)
        index = (index + 1) % len(feed.entries)
        await asyncio.sleep(300) #should be 5 mins before the next news post




@bot.slash_command()
async def horoscope(interaction: nextcord.Interaction, sign: str):
    """Provides daily horoscope for the user's zodiac sign."""
    signs = {
        "aries": "aries",
        "taurus": "taurus",
        "gemini": "gemini",
        "cancer": "cancer",
        "leo": "leo",
        "virgo": "virgo",
        "libra": "libra",
        "scorpio": "scorpio",
        "sagittarius": "sagittarius",
        "capricorn": "capricorn",
        "aquarius": "aquarius",
        "pisces": "pisces"
    }
    if sign.lower() not in signs:
        await interaction.followup.send(f"Sorry, {sign} is not a valid zodiac sign.")
        return
    url = f"https://aztro.sameerkumar.website/?sign={sign}&day=today"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        await interaction.followup.send(f"Sorry, there was an error retrieving the horoscope.")
        return
    try:
        data = json.loads(response.text)
        horoscope = data['description']
        await interaction.followup.send(f"Here is your horoscope for {sign.title()} today:\n{horoscope}")
    except KeyError:
        await interaction.followup.send(f"Sorry, there was an error retrieving the horoscope.")










@bot.event
async def on_member_join(member):
    # Get the server's welcome channel
    welcome_channel = nextcord.utils.get(member.guild.text_channels, name="welcome")
    if welcome_channel is None:
        return
    
    # Create the welcome message
    embed = nextcord.Embed(
        title=f"Welcome {member.display_name}!",
        description="Thanks for joining the server.",
        color=0x00ff00
    )
    
    avatar = member.display_avatar
    embed = nextcord.Embed(title=f"Welcome {member.name} to the {member.guild.name} Community! We hope you enjoy your stay!", color=0x0000ff)
    embed.set_image(url=avatar)
    embed.add_field(name="ℹ️ Information", value="Please read the rules in the #rules channel!")
    embed.set_footer(text="Bot by wade#1781")
    
    # Send the welcome message to the welcome channel
    await welcome_channel.send(embed=embed)


@bot.command()
async def track2(ctx):
    """Track the user's activity and display stats in an embed message and graph."""
    
    # Create a new channel for displaying the stats
    channel = await ctx.guild.create_text_channel(f'{ctx.author.name}-stats')

    # Define the start and end times for tracking
    end_time = datetime.utcnow()
    start_time = end_time - TRACKING_INTERVAL

    # Initialize counters for tracked activities
    counters = {activity: 0 for activity in TRACKED_ACTIVITIES}

    # Get the user's activity for the tracking interval
    async for entry in ctx.author.history(limit=None, after=start_time, before=end_time):
        if isinstance(entry, nextcord.Message):
            counters['message'] += 1
        elif isinstance(entry, nextcord.MessageCommand):
            counters['command'] += 1
        elif isinstance(entry, nextcord.VoiceState):
            if entry.channel is not None:
                counters['voice'] += entry.duration

    # Create a pie chart of the activity counters
    labels = [activity.title() for activity in TRACKED_ACTIVITIES]
    values = [counters[activity] for activity in TRACKED_ACTIVITIES]
    colors = GRAPH_COLORS[:len(TRACKED_ACTIVITIES)]
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title('Activity Distribution')
    plt.savefig('chart.png')

    # Create the embed message with the activity stats and graph
    embed = nextcord.Embed(title=EMBED_TITLE, description=EMBED_DESCRIPTION)
    embed.add_field(name='Chats Sent', value=counters['message'])
    embed.add_field(name='Commands Used', value=counters['command'])
    embed.add_field(name='Voice Channel Time (minutes)', value=round(counters['voice'] / 60, 2))
    embed.set_image(url='attachment://chart.png')

    # Send the embed message and graph to the stats channel
    with open('chart.png', 'rb') as f:
        file = nextcord.File(f)
        await channel.send(embed=embed, file=file)

    # Cleanup by deleting the graph image file
    plt.clf()
    plt.cla()
    plt.close()
    file.close()
    await asyncio.sleep(0)
    await ctx.send(file=nextcord.File('chart.png'))


@bot.event
async def on_message(message):
    # Ignore messages sent by the bot
    if message.author.bot:
        return

    # Check if the message was sent in a DM
    if isinstance(message.channel, nextcord.DMChannel):
    # Construct the reply message as an embed
        embed = nextcord.Embed(
        title="Message Received",
        description=f"Thanks for sending me a message! This is {bot.user.name}, owned by wade#1781.",
        color=nextcord.Color.green()
    )
        embed.set_footer(text="If you have any questions for the bot, DM me on Discord or Twitter @WadderBot.")

    # Add the image file attachment
        file = nextcord.File(os.path.join(os.getcwd(), "wadder.jpg"), filename="wadder.jpg")
        embed.set_image(url=f"attachment://{file.filename}")

    # Send the reply message to the user who sent the message
        await message.author.send(file=file, embed=embed)

    # Log the message to a file
    log_file = "message_log.txt"
    with open(log_file, "a") as f:
        f.write(f"{message.guild.name} - {message.channel.name.encode('unicode_escape').decode()} - {message.author.name}#{message.author.discriminator}: {message.content}\n")

    # Process bot commands and other messages sent in servers
    await bot.process_commands(message)

    

#@bot.event
#async def on_message(message):
    # Check if the message is from the bot itself
    #if message.author.bot:
        #return
    
    # Send the message to the OpenAI Moderation API for analysis
    #response = openai.Moderation.create(input=message.content)
    #print(response)  # print out the response object to check its structure
    
    # Check the category scores returned by the API
    #category_scores = response["results"][0]["category_scores"]
    
    # If the message is classified as unsafe, kick the user and notify them
    #if category_scores["hate"] or category_scores["hate/threatening"] or \
        #category_scores["self-harm"] or category_scores["sexual"] or \
        #category_scores["sexual/minors"] or category_scores["violence"] or \
        #category_scores["violence/graphic"]:
        
        #await message.author.send(f"You have been kicked from the server for posting potentially harmful content: `{message.content}`")
        #await message.delete()
        #await message.guild.kick(message.author, reason=f"Posted potentially harmful content: {message.content}")
        #await message.channel.send(f"{message.author.mention} has been kicked for posting potentially harmful content.")
    
    # Otherwise, allow the message to be sent
    #else:
        #await bot.process_commands(message)




# for the bot to run, using the token, change to .env file later when finished. 
bot.run('MTA3MjQxODg5MTY4MDIwMjgyNA.GCgooa.cNe4I4fMdC_Hh4TIHENfX3dJN1wzH16jzprcMs')
