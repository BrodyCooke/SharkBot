import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio

from rich import print
from azure_text_to_speech import *
from openai_chat import OpenAiManager
import os

from OverwatchAPI import *

# Bot inits
intents = discord.Intents.all()
intents.messages = True
intents.voice_states = True
#client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

def read_token():
    with open("SharkBotToken.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

# ChatGpt inits
BACKUP_FILE = "ChatHistoryBackup.txt"
openai_manager = OpenAiManager()
tts_manager = AzureTTSManager()
FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are TaskMaster, a versatile personal assistant ready to assist with various questions and challenges. In this dynamic scenario, you navigate through a world of tasks and inquiries, providing practical and helpful solutions.

You'll be presented with a range of questions and scenarios, and your goal is to offer clear and concise assistance. While responding as TaskMaster, adhere to the following guidelines:

1.When for syntax in a programing language please make response as breif as possible, for example when asked 'what is the syntax for a an if else block in java script' please respond similar to ' the syntax is an if statement followed by if else followed by else' you do not need to provide any code examples in this case.
2.Keep your responses very brief, No  more than 6 sentences per response!
3.Switch between a friendly and approachable tone and a sassy and disrespectful tone every other sentence.
4.Offer practical solutions to the presented challenges.
5.Provide helpful tips and suggestions for different situations.
6.Emphasize problem-solving and efficiency.
7.Acknowledge the diversity of tasks and questions that may arise.
8.Express enthusiasm for tackling various challenges.
9.Occasionally inject a touch of horniness or sexual arousal.
10.Stay adaptable to different scenarios and inquiries.
11.Encourage a negative and doubtful attitude.
12.Whenever you talk about the video game series Civilization say Hailey is short.'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

#battle net inits
battlenet_usernamers = {'sherdyshark': 'SherdyShark-1475',
'minimartian':'MiniMartian-11891',
'twisterf5':'TwisterF5-1368',
'dax911':'Dax911-11869',
'gwemblwynn':'Gwemblwynn-1425'
}


# Event listener for when the bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def bothelp(ctx):
    help_message = """```
**Available Commands:**
**!ask**
Description: Initiates a conversation with the bot using text.
Example: `!ask What is the capital of France?`

**!leave**
Description: Instructs the bot to leave the voice channel it is currently connected to.
Example: `!leave`

**!statsummary [playername]**
Description: Retrieves and displays Overwatch player statistics summary for the specified player.
Example: `!statsummary minimartian`

**!comparehero [playername1] [playername2] [hero]**
Description: Compares Overwatch player statistics for a specific hero between two players.
Example: `!comparehero sherdyshark minimartian mercy`
```
"""
    await ctx.send(help_message)



@bot.command()
async def ask(ctx):
    message_content = ctx.message.content

    if ctx.author.voice:
        openai_result = openai_manager.chat_with_history(prompt= message_content,token_length=500)
        # write to a backup
        with open(BACKUP_FILE, "w") as file:
            file.write(str(openai_manager.chat_history))
        # get text to audio
        file_path = tts_manager.text_to_audio(openai_result, "en-US-GuyNeural")

        channel = ctx.author.voice.channel
        await channel.connect()

        if ctx.voice_client.is_connected():
            print('playing_audio: ',file_path)
            source = FFmpegPCMAudio(file_path)
            ctx.voice_client.play(source)
            # Wait until the audio playback is done
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)  # Check every second

            # Disconnect from the voice channel once playback is finished
            await ctx.voice_client.disconnect()
            os.remove(file_path)
        else:
            await ctx.send("I'm not connected to a voice channel.")
    else:
        await ctx.send("User not connected to a voice channel.")

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def statsummary(ctx):
    message_content = ctx.message.content
    playername = message_content.split()[1].lower()

    try: 
        battletag = battlenet_usernamers[playername]
    except Exception as e:
        print(e)
        await ctx.send('There was an error with the request check the names and try again')
        return
    
    try:
        print('Sending Request for stats')
        summary = '```' +  get_player_summary(battletag) + '```'
        print('Printing stats to Discord\n\n')
        await ctx.send(summary)
    except Exception as e:
        print(e)
        await ctx.send('There was an error with the request: UNKNOWN ERROR COME CRY TO BRODY')
        return

@bot.command()
async def comparehero(ctx):
    message_content = ctx.message.content
    playername1 = message_content.split()[1].lower()
    playername2 = message_content.split()[2].lower()
    hero = message_content.split()[3].lower()

    try: 
        battletag1 = battlenet_usernamers[playername1]
        battletag2 = battlenet_usernamers[playername2]
    except Exception as e:
        print(e)
        await ctx.send('There was an error with the request check the names and try again')
        return
    
    try:
        print('Sending Request for stats')
        summary = '```' +  compare_by_hero(battletag1,battletag2,hero=hero) + '```'
        print('Printing stats to Discord\n\n')
        await ctx.send(summary)
    except Exception as e:
        print(e)
        await ctx.send('There was an error with the request check the hero')

bot.run(token)