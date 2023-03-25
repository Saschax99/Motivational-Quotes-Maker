import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)  # changes the voice
   engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()


# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
  
# for voice in voices:
#     # to get the info. about various voices in our PC 
#     print(voice)
#     print("ID: %s" %voice.id)
#     print("Name: %s" %voice.name)
#     print("Age: %s" %voice.age)
#     print("Gender: %s" %voice.gender)
#     print("Languages Known: %s" %voice.languages)
