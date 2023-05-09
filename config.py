import os

YOUTUBE_USER = "x"
YOUTUBE_PASSWORD = "x"

INSTA_USER = "x"
INSTA_PASSWORD = "x"

SONGS_PATH = "./songs"
TEMP_PATH = os.path.join("temp")
TEMP_TTS_PATH = os.path.join("temp", "tts")
TEMP_CUT_VIDEO_PATH = os.path.join("temp", "cut_video")
TEMP_VIDEO_TEXT_PATH = os.path.join("temp", "video_text")
RESULTS_PATH = os.path.join("results")
QUOTES_PATH = os.path.join("assets", "quotes")  # path where an file exists in a json format with e. g. "element": {"image": "", "content": "", "autor": ""} format
BACKGROUND_VIDEOS_PATH = os.path.join("assets", "background_videos")
BACKGROUND_MUSIC_PATH = os.path.join("assets", "background_music")
TEMPLATE_INTRO_PATH = os.path.join("assets", "templates", "intro.mp4")
TEMPLATE_OUTRO_PATH = os.path.join("assets", "templates", "outro.mp4")
TTS_EXTENSION = '.wav'
MUSIC_EXTENSION = '.mp3'
VIDEO_EXTENSION = '.mp4'

TIMEOUT = 30
AUDIO_LENGTH_OFFSET = 2
