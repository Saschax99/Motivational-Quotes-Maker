from scripts.tts.tts_generator import VoiceGenerator
from scripts.editing.video_editing import VideoEdit

from scripts.uploader.youtube_uploader import YoutubeShortsUploader
from scripts.uploader.instagram_uploader import InstagramShortsUploader
from scripts.utils.omp_tools import OsTools
import config
import os
import random

text_title = '''
  ______ _                               _______                                                
 / _____) |                  _          (_______)                                _              
( (____ | |__   ___   ____ _| |_  ___    _   ___ _____ ____  _____  ____ _____ _| |_ ___   ____ 
 \____ \|  _ \ / _ \ / ___|_   _)/___)  | | (_  | ___ |  _ \| ___ |/ ___|____ (_   _) _ \ / ___)
 _____) ) | | | |_| | |     | |_|___ |  | |___) | ____| | | | ____| |   / ___ | | || |_| | |    
(______/|_| |_|\___/|_|      \__|___/    \_____/|_____)_| |_|_____)_|   \_____|  \__)___/|_|
'''

text_path = os.path.join("assets", "quotes")  # path where an file exists in a json format with e. g. "element": {"image": "", "content": "", "autor": ""} format
output_path = os.path.join("results")
temp_path = os.path.join("temp")
background_videos = os.path.join("assets", "background_videos")

def create_video_with_tts_and_text(content, author):
    selected_video = random.choice(os.listdir(background_videos))  # select background video
    video_path = os.path.abspath(os.path.join(background_videos, selected_video))  # get video path of the selected video
    
    output_default_name = f"{OsTools.generate_id(10)}_{author}"  # get outputs default name id + author
    result_output_path = os.path.join(output_path, output_default_name)  # get results path with default output name
    temp_output_path = os.path.join(temp_path, output_default_name)  # get temp path with default output name
    print(video_path)
    
    content = OsTools.delete_unreadable_characters(content, [";", "”", "“"])
    VoiceGenerator().tts(content, temp_output_path + ".wav")
    VideoEdit().add_text_to_vertical_video(video_path, content, author, result_output_path + ".mp4")
    exit()
    pass

if __name__ == '__main__':
    print(text_title)
    print("Shorts Generator - By Saschax", "\nThe program automatically generates videos with tts and displaying texts to download and edit the videos with music that are in the /songs directory. These videos can then be uploaded to Youtube/Instagram/TikTok. Using pexels.com as reference")
    
    print(f"selecting '{text_path}' as path..", end=" ")
    if OsTools.get_folder_count(text_path, "json"):
        file_path = os.path.join(text_path, os.listdir(text_path)[0])
        print(f"selected file in '{file_path}'")
    else:
        raise AssertionError(f"no json file found in '{text_path}'.")
            
    data = OsTools.read_file(file_path)
    for element in data:
        content = element.get("element").get("content")        
        author = element.get("element").get("autor")  # missspelled..
        print(content, author)
        
        status = create_video_with_tts_and_text(content, author)
        
    # amount = str(input("amount of videos to upload [new account limit=10]: "))
    # try:
    #     user = config.YOUTUBE_USER
    #     password = config.YOUTUBE_PASSWORD
    # except:
    #     user = str(input("username of youtube: "))
    #     password = str(input("password of youtube: "))
    # ytUploader = YoutubeShortsUploader(amount, user, password, True)
    # ytUploader.get_browser()
    # ytUploader.upload_video_series()
