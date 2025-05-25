import whisper

class SpeechService:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, filepath):
        return self.model.transcribe(filepath)
