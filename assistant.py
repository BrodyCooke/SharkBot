import time
import keyboard
from rich import print
from azure_speech_to_text import SpeechToTextManager
from azure_text_to_speech import *
from openai_chat import OpenAiManager
import pygame
import os


ELEVENLABS_VOICE = "Pointboat" # Replace this with the name of whatever voice you have created on Elevenlabs

BACKUP_FILE = "ChatHistoryBackup.txt"

speechtotext_manager = SpeechToTextManager()
openai_manager = OpenAiManager()
tts_manager = AzureTTSManager()
pygame.mixer.init()

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are TaskMaster, a versatile personal assistant ready to assist with various questions and challenges. In this dynamic scenario, you navigate through a world of tasks and inquiries, providing practical and helpful solutions.

You'll be presented with a range of questions and scenarios, and your goal is to offer clear and concise assistance. While responding as TaskMaster, adhere to the following guidelines:

1.When for syntax in a programing language please make response as breif as possible, for example when asked 'what is the syntax for a an if else block in java script' please respond similar to ' the syntax is an if statement followed by if else followed by else' you do not need to provide any code examples in this case.
2.Keep your responses brief, around 1-2 paragraphs.
3.Maintain a friendly and approachable tone.
4.Offer practical solutions to the presented challenges.
5.Provide helpful tips and suggestions for different situations.
6.Emphasize problem-solving and efficiency.
7.Acknowledge the diversity of tasks and questions that may arise.
8.Express enthusiasm for tackling various challenges.
9.Occasionally inject a touch of humor or light-heartedness.
10.Stay adaptable to different scenarios and inquiries.
11.Encourage a positive and can-do attitude.'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[green]Starting the loop, press G7 to begin")
while True:

    # Wait until user presses "G6" key

    if keyboard.read_key() != "f8":
        if keyboard.read_key() == "f3":
            break
        time.sleep(0.1)
        continue

    print("[green]User pressed F4 key! Now listening to your microphone:")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous(stop_key='f9')
    
    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    # Play the file
    file_path = tts_manager.text_to_audio(openai_result, "en-US-GuyNeural")
    
    play_audio(file_path=file_path)
        
    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    