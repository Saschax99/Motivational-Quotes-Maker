from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager

def select_key_value_by_index(dictionary, number):
    for index, (key, value) in enumerate(dictionary.items()):
        if index == number:
            return key, value

class VoiceGenerator:
    def __init__(self):
        self.path = "C:/Users/dolsa/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0/LocalCache/local-packages/Python38/site-packages/TTS/.models.json"        
        self.model_manager = ModelManager(self.path)

        model_path, config_path, model_item = self.model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")
        voc_path, voc_config_path, _ = self.model_manager.download_model("vocoder_models/en/ljspeech/hifigan_v2")

        self.syn = Synthesizer(
            tts_checkpoint=model_path,
            tts_config_path=config_path,
            vocoder_checkpoint=voc_path,
            vocoder_config=voc_config_path
        )
        
    def generate_tts(self, text, output_directory):
        outputs = self.syn.tts(text)
        self.syn.save_wav(outputs, output_directory)

if __name__ == '__main__':
    voicegen = VoiceGenerator()
    voicegen.tts("Be yourself; everyone else is already taken. This is going to be used for Youtube tts", 
                "output.wav")
