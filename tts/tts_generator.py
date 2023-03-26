from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager

path = "C:/Users/dolsa/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0/LocalCache/local-packages/Python38/site-packages/TTS/.models.json"

model_manager = ModelManager(path)

model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")

voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])

syn = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path
)

text = "Hello from a machine"

outputs = syn.tts(text)
syn.save_wav(outputs, "audio-1.wav")



# initialize the synthesizer with the name of the model and the name of the voice
# synthesizer = Synthesizer("tts_models/en/ljspeech/tacotron2-DDC/config.json", "tts_models/en/ljspeech/glow-tts/glow-tts.pth.tar", "ljspeech")

# # generate speech from text
# text = "Hello, world!"
# audio = synthesizer.synthesize(text)

# # save the audio to a file
# with open("output.wav", "wb") as f:
#     f.write(audio)
    
    
    #tts --text "hello this is my first test with tts" --model_path "ljspeech tacotron2/model_file.pth.tar" --config_path "ljspeech tacotron2/config.json" --out_path "output.wav"
