import discord
from discord.ext import commands
import asyncio

# Set up the bot with the prefix you want to use for commands
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.reactions = True

bot = commands.Bot(command_prefix='suntoolkit!', intents=intents)

@bot.event
async def on_ready():
    print(f'SunToolkit started as {bot.user}')

# Specific channel IDs
SOURCE_CHANNEL_ID = CHANNEL-ID  # Replace with the ID of the channel where the command can be executed
DESTINATION_CHANNEL_ID = CHANNEL-ID  # Replace with the ID of the rules channel

# Command to send rules to the rules channel
@bot.command()
async def srv_rules(ctx):
    # Check if the command was sent in the specific channel
    if ctx.channel.id != SOURCE_CHANNEL_ID:
        await ctx.send("`ERROR: This command can only be used in the bot-command-prompt channel.`")
        return

    # Get the destination channel
    destination_channel = bot.get_channel(DESTINATION_CHANNEL_ID)
    if not destination_channel:
        await ctx.send("`ERROR: Could not find the destination channel. Please check the bot configuration.`")
        return
    
    # Send a message requesting the rules
    message = await ctx.send("Ok! Reply to this message with the server rules, and I will send them to the rules channel.")

    # Wait for the user's response
    def check(m):
        return m.reference and m.reference.message_id == message.id and m.author == ctx.author

    try:
        response = await bot.wait_for('message', timeout=300.0, check=check)  # 300 seconds (5 minutes) wait time
        rules = response.content

        # Send the rules to the destination channel
        await destination_channel.send(rules)
        await ctx.send(f"The rules have been successfully sent to {destination_channel.mention}.")
    except asyncio.TimeoutError:
        await ctx.send("`ERROR: Response time exceeded.`")


# Command to test if the bot is working
@bot.command()
async def test(ctx):
    await ctx.send("it works!")

# Run the bot (replace "TOKEN" with your token. https://discord.com/developers/applications)
bot.run('TOKEN')
