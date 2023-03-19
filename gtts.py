from gtts import gTTS
#tts = gTTS('hello how are you bro')

tts = gTTS('hello how are you', lang='en', tld='com.au')
tts.save('hello.mp3')