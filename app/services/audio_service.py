from pydub import AudioSegment
import librosa
import os
import uuid

class AudioService:
    def convert_to_wav(self, input_path: str, output_path: str):
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="wav")
        return output_path

    def get_duration(self, path: str):
        y, sr = librosa.load(path)
        return librosa.get_duration(y=y, sr=sr)

    def preprocess(self, input_path: str) -> str:
        """Обрабатывает входной файл и конвертирует в WAV"""
        ext = os.path.splitext(input_path)[-1]
        if ext.lower() == ".wav":
            return input_path

        output_path = f"{os.path.splitext(input_path)[0]}_{uuid.uuid4().hex}.wav"
        return self.convert_to_wav(input_path, output_path)
