from pytube import YouTube
import moviepy.editor as mp
import speech_recognition as sr
import os
from langdetect import detect
import logging
from pydub import AudioSegment
import time
import whisper


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL = whisper.load_model("medium")

class YoutubeHandler:

    def init(self):
      pass

    def convert_video_to_audio(self,video_link):
        try:
            yt_video = YouTube(video_link)
            stream = yt_video.streams.filter(only_audio=True).first()
            output_file = stream.download(filename='audio.mp4')

            audio_clip = mp.AudioFileClip(output_file)
            audio_file = 'audio.wav'
            audio_clip.write_audiofile(audio_file)
            return audio_file , output_file

        except Exception as e:
            print("Error while converting video to audio: ", e)

        

    def convert_audio_to_text (self , audio_file):

        try:
            result = MODEL.transcribe(audio_file)
            text_file = "app\cache\Text.txt"
            with open(text_file, "w") as file:
                file.write(result["text"])

            text_language = result["language"]
            return  text_language , text_file

        except Exception as e:
            print("Error while converting audio to text: ", e)

      

    def convert_video_to_text(self, video_link):
        try:
            audio_file , output_file = self.convert_video_to_audio(video_link)

            text_language , text_file  = self.convert_audio_to_text(output_file)

            return text_file,text_language
                     
                    
                
        
        except Exception as e:
            print("Error while converting video to text: ", e)


