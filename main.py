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


def create_video_with_tts_and_text(index, content, author):
    selected_background_video = random.choice(os.listdir(config.BACKGROUND_VIDEOS_PATH))  # select background video
    selected_background_video_path = os.path.abspath(
        os.path.join(config.BACKGROUND_VIDEOS_PATH, selected_background_video))  # get video path of the selected video

    generated_file_name = f"{index}_{OsTools.generate_id(10)}_{author}"  # get outputs default name id + author

    result_output_path = os.path.join(config.RESULTS_PATH,
                                      generated_file_name) + config.VIDEO_EXTENSION  # get results path with default output name
    temp_tts_output_path = os.path.join(config.TEMP_TTS_PATH, generated_file_name) + config.TTS_EXTENSION
    temp_cut_video_output_path = os.path.join(config.TEMP_CUT_VIDEO_PATH, generated_file_name) + config.VIDEO_EXTENSION
    temp_text_video_output_path = os.path.join(config.TEMP_VIDEO_TEXT_PATH,
                                               generated_file_name) + config.VIDEO_EXTENSION

    content = OsTools.delete_unreadable_characters(content, [";", "”", "“"])
    if len(content) >= 250 or content is None:
        print(f"skipping '{content}' because its too long or is None")
        return None

    voicegen = VoiceGenerator()
    videoedit = VideoEdit()

    videoedit.add_text_to_vertical_video(selected_background_video_path, content, author, temp_text_video_output_path)
    voicegen.generate_tts(content, temp_tts_output_path)
    duration = videoedit.get_audio_length(temp_tts_output_path)  # get duration of audio
    videoedit.cut_video(0, round(duration + config.AUDIO_LENGTH_OFFSET), temp_text_video_output_path,
                        temp_cut_video_output_path, config.TEMPLATE_INTRO_PATH,
                        config.TEMPLATE_OUTRO_PATH)  # cut selected video with tts length + offset

    selected_background_music = random.choice(os.listdir(config.BACKGROUND_MUSIC_PATH))
    selected_background_music_path = os.path.join(config.BACKGROUND_MUSIC_PATH, selected_background_music)
    videoedit.add_audio_clips_to_video(temp_cut_video_output_path, temp_tts_output_path, selected_background_music_path,
                                       result_output_path)

    OsTools.delete_files(temp_tts_output_path, temp_cut_video_output_path, temp_text_video_output_path)
    return result_output_path


if __name__ == '__main__':
    print(text_title)
    print("Shorts Generator - By Saschax",
          "\nThe program automatically generates videos with tts and displaying texts to download and edit the videos with music that are in the /songs directory. These videos can then be uploaded to Youtube/Instagram/TikTok. Using pexels.com as reference")

    print(f"selecting '{config.QUOTES_PATH}' as path..", end=" ")
    if OsTools.get_folder_count(config.QUOTES_PATH, "json"):
        file_path = os.path.join(config.QUOTES_PATH, os.listdir(config.QUOTES_PATH)[0])  # select first file in path
        print(f"selected file in '{file_path}'")
    else:
        raise AssertionError(f"no json file found in '{config.QUOTES_PATH}'.")

    data = OsTools.read_file(file_path)
    for index, element in enumerate(data):
        if index <= 20:
            continue
        content = element.get("element").get("content")
        author = element.get("element").get("autor")  # missspelled..
        print(content, author)
        output = create_video_with_tts_and_text(index, content, author)
        # if os.path.exists(output):
        #     OsTools.remove_first_element_in_file(file_path)
        # else:
        #     print(f"keyword '{content}' with index {index} too long or couldnt create video")

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
