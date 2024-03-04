import os
import random
import azure.cognitiveservices.speech as speechsdk
from gtts import gTTS
from pydub import AudioSegment
import time
import soundfile as sf
from mutagen.mp3 import MP3
import pygame

AZURE_VOICES = [
    "en-US-DavisNeural",
    "en-US-TonyNeural",
    "en-US-JasonNeural",
    "en-US-GuyNeural",
    "en-US-JaneNeural",
    "en-US-NancyNeural",
    "en-US-JennyNeural",
    "en-US-AriaNeural",
]

AZURE_VOICE_STYLES = [
    # Currently using the 9 of the 11 available voice styles
    # Note that certain styles aren't available on all voices
    "angry",
    "cheerful",
    "excited",
    "hopeful",
    "sad",
    "shouting",
    "terrified",
    "unfriendly",
    "whispering"
]

AZURE_PREFIXES = {
    "(angry)" : "angry",
    "(cheerful)" : "cheerful",
    "(excited)" : "excited",
    "(hopeful)" : "hopeful",
    "(sad)" : "sad",
    "(shouting)" : "shouting",
    "(shout)" : "shouting",
    "(terrified)" : "terrified",
    "(unfriendly)" : "unfriendly",
    "(whispering)" : "whispering",
    "(whisper)" : "whispering",
    "(random)" : "random"
}

class AzureTTSManager:
    azure_speechconfig = None
    azure_synthesizer = None

    def __init__(self):
        pygame.init()
        # Creates an instance of a speech config with specified subscription key and service region.
        # Replace with your own subscription key and service region (e.g., "westus").
        self.azure_speechconfig = speechsdk.SpeechConfig(subscription=os.getenv('SPEECH_KEY'), region=os.getenv('SPEECH_REGION'))
        # Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
        self.azure_speechconfig.speech_synthesis_voice_name = "en-US-AriaNeural"
        # Creates a speech synthesizer. Setting audio_config to None means it wont play the synthesized text out loud.
        self.azure_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.azure_speechconfig, audio_config=None)        

    # Returns the path to the new .wav file
    def text_to_audio(self, text: str, voice_name="random", voice_style="hopeful"):
        if voice_name == "random":
            voice_name = random.choice(AZURE_VOICES)
        if voice_style == "random":
            voice_style = random.choice(AZURE_VOICE_STYLES)

        # Change the voice style if the message includes a prefix
        text = text.lower()
        if text.startswith("(") and ")" in text:
            prefix = text[0:(text.find(")")+1)]
            if prefix in AZURE_PREFIXES:
                voice_style = AZURE_PREFIXES[prefix]
                text = text.removeprefix(prefix)
        if len(text) == 0:
            print("This message was empty")
            return
        if voice_style == "random":
            voice_style = random.choice(AZURE_VOICE_STYLES)

        ssml_text = f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xmlns:emo='http://www.w3.org/2009/10/emotionml' xml:lang='en-US'>
        <voice name='{voice_name}'>
        <mstts:express-as style='{voice_style}'>
        <prosody rate='1.25'>
        {text}
        </prosody>
        </mstts:express-as>
        </voice>
        </speak>"""
        result = self.azure_synthesizer.speak_ssml_async(ssml_text).get()

        output = os.path.join(os.path.abspath(os.curdir), f"_Msg{str(hash(text))}{str(hash(voice_name))}{str(hash(voice_style))}.wav")
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            stream = speechsdk.AudioDataStream(result)
            stream.save_to_wav_file(output)
        else:
            # If Azure fails, use gTTS instead. gTTS saves as an mp3 by default, so convert it to a wav file after
            print("\n   Azure failed, using gTTS instead   \n")
            output_mp3 = output.replace(".wav", ".mp3")
            msgAudio = gTTS(text=text, lang='en', slow=False)
            msgAudio.save(output_mp3)
            audiosegments = AudioSegment.from_mp3(output_mp3)
            audiosegments.export(output, format="wav")

        return output
    
def play_audio(file_path, sleep_during_playback=True, delete_file=True, play_using_music=True):
        """
        Parameters:
        file_path (str): path to the audio file
        sleep_during_playback (bool): means program will wait for length of audio file before returning
        delete_file (bool): means file is deleted after playback (note that this shouldn't be used for multithreaded function calls)
        play_using_music (bool): means it will use Pygame Music, if false then uses pygame Sound instead
        """
        print(f"Playing file with pygame: {file_path}")
        pygame.mixer.init()
        if play_using_music:
            # Pygame Mixer only plays one file at a time, but audio doesn't glitch
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        else:
            # Pygame Sound lets you play multiple sounds simultaneously, but the audio glitches for longer files
            pygame_sound = pygame.mixer.Sound(file_path) 
            pygame_sound.play()

        if sleep_during_playback:
            # Calculate length of the file, based on the file format
            _, ext = os.path.splitext(file_path) # Get the extension of this file
            if ext.lower() == '.wav':
                wav_file = sf.SoundFile(file_path)
                file_length = wav_file.frames / wav_file.samplerate
                wav_file.close()
            elif ext.lower() == '.mp3':
                mp3_file = MP3(file_path)
                file_length = mp3_file.info.length
            else:
                print("Cannot play audio, unknown file type")
                return

            # Sleep until file is done playing
            time.sleep(file_length)

            # Delete the file
            if delete_file:
                # Stop pygame so file can be deleted
                # Note, this can cause issues if this function is being run on multiple threads, since it quit the mixer for the other threads too
                pygame.mixer.music.stop()
                pygame.mixer.quit()

                try:  
                    #os.remove(file_path)
                    print(f"Deleted the audio file.")
                except PermissionError:
                    print(f"Couldn't remove {file_path} because it is being used by another process.")


# Tests here
if __name__ == '__main__':
    tts_manager = AzureTTSManager()
    pygame.mixer.init()

    file_path = tts_manager.text_to_audio("Imagine a chessboard that bridges the charm of traditional gameplay with the cutting-edge technology of the 21st century. Our team has developed an electronic and autonomous chessboard that revolutionizes the way chess is experienced. Unlike standard boards, our creation offers a unique blend of manual and automated play. You can move the pieces yourself, or watch in awe as they glide across the board autonomously. This isn’t just a chessboard; it's a smart, interactive platform you can play against a formidable computer opponent with several different skill levels, or challenge friends and family, whether they're in the same room or halfway across the world. Our board offers the tactile satisfaction of physical chess pieces, combined with the convenience and connectivity of digital gaming", "en-US-GuyNeural")
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while True:
        stuff_to_say = input("\nNext question? \n\n")
        if len(stuff_to_say) == 0:
            continue
        file_path = tts_manager.text_to_audio(stuff_to_say)
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        