from gtts import gTTS
from pathlib import Path
from mutagen.mp3 import MP3
from utils.console import print_step, print_substep
from rich.progress import track
import azure.cognitiveservices.speech as speechsdk
def save_text_to_mp3(reddit_obj):
    """Saves Text to MP3 files.

    Args:
        reddit_obj : The reddit object you received from the reddit API in the askreddit.py file.
    """
    speech_config = speechsdk.SpeechConfig(subscription="", region="")
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    file_name = "assets/mp3/title.mp3"
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
    print_step("Saving Text to MP3 files...")
    length = 0

    # Create a folder for the mp3 files.
    Path("assets/mp3").mkdir(parents=True, exist_ok=True)

    #tts = gTTS(text=reddit_obj["thread_title"], lang="en", slow=False)
    tts = speech_synthesizer.speak_text_async(reddit_obj["thread_title"]).get()
    #tts.save(f"assets/mp3/title.mp3")
    tts = speechsdk.AudioDataStream(tts)
    #tts.save_to_wav_file("assets/mp3/title.mp3")
    length += MP3(f"assets/mp3/title.mp3").info.length
    
    for idx, comment in track(enumerate(reddit_obj["comments"]), "Saving..."):
        # ! Stop creating mp3 files if the length is greater than 50 seconds. This can be longer, but this is just a good starting point
        if length > 50:
            break
        #tts = gTTS(text=comment["comment_body"], lang="en", slow=False)
        file_name = (f"assets/mp3/{idx}.mp3")
        file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
        tts = speech_synthesizer.speak_text_async(comment["comment_body"]).get()
        #tts.save(f"assets/mp3/{idx}.mp3")
        tts = speechsdk.AudioDataStream(tts)
        tts.save_to_wav_file(f"assets/mp3/{idx}.mp3")
        length += MP3(f"assets/mp3/{idx}.mp3").info.length


    print_substep("Saved Text to MP3 files successfully.", style="bold green")
    # ! Return the index so we know how many screenshots of comments we need to make.
    return length, idx
