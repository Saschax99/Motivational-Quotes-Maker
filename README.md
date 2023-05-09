# Youtube-Affiliate-Maker
this program creates videos with tts, text, intro + outro, background music and background video

## text to speech
### tts setup
model: tts_models/en/ljspeech/tacotron2-DDC
vocoder: vocoder_models/en/ljspeech/hifigan_v2
### usage
tts is used to generate a voice for shorts videos e. g. motivational videos

## displaying text
### setup
displaying white text on black/transparent background
limited keywords
### usage
displaying automatically text in correct format
displaying text one by one for pretty animation instead of displaying it instantly

## intro and outro
### usage
implementing an intro and outro to the main video
## background music
### usage
selecting random music from music folder and adding it to the video
## background video
### usage
adding background video to the main video e. g. subway surfers


## commands
### starting virtual enviroment
python -m venv myenv
myenv/Scripts/activate
deactivate
### installing tts
python3 -m pip install TTS
### list all tts models
tts --list_models
### formatting videos into 1080x1920 ratio
ffmpeg -i INPUT.mp4 -acodec copy -crf 12 -vf scale=1080:1920,setsar=1:1 output.mp4
