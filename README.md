# Youtube-Affiliate-Maker

python -m venv myenv

myenv/Scripts/activate

install TTS
	python3 -m pip install TTS

deactivate

outside of venv

tts --list_models



format video to 1080x1920 ratio

ffmpeg -i INPUT.mp4 -acodec copy -crf 12 -vf scale=1080:1920,setsar=1:1 output.mp4
