import os
import uuid
import subprocess
from typing import List
from app.logger import celery_logger
from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
from pydub import AudioSegment

class AudioService:
    def __init__(self):
        self.tmp_root = "/tmp/audio_chunks"
        os.makedirs(self.tmp_root, exist_ok=True)
        self.vad_model = load_silero_vad()

    def split_audio(self, input_path: str, chunk_length: int = 60) -> List[str]:
        celery_logger.info(f"Деление {input_path} на чанки по {chunk_length} сек.")
        chunk_id = uuid.uuid4().hex
        output_dir = os.path.join(self.tmp_root, chunk_id)
        os.makedirs(output_dir, exist_ok=True)

        ext = os.path.splitext(input_path)[-1]
        chunk_template = os.path.join(output_dir, "chunk_%03d" + ext)

        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-i", input_path,
            "-f", "segment",
            "-segment_time", str(chunk_length),
            "-c", "copy",
            chunk_template
        ], check=True)

        chunk_paths = sorted([
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if os.path.isfile(os.path.join(output_dir, f))
        ])

        return chunk_paths

    def convert_to_wav(self, input_path: str, output_path: str) -> str:
        try:
            subprocess.run([
                "ffmpeg", "-y",  # авто-перезапись
                "-hide_banner", "-loglevel", "error",
                "-i", input_path,
                "-ar", "16000", "-ac", "1",
                output_path
            ], check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            celery_logger.error(f"Ошибка при конвертации {input_path} в WAV: {e}")
            raise

    def apply_vad(self, wav_path: str) -> str:
        celery_logger.info(f"Применение VAD к {wav_path}")
        wav_tensor = read_audio(wav_path)
        speech_timestamps = get_speech_timestamps(wav_tensor, self.vad_model, return_seconds=True)

        if not speech_timestamps:
            celery_logger.warning(f"Речь не найдена в {wav_path}, возвращаем оригинал")
            return wav_path

        audio = AudioSegment.from_wav(wav_path)
        speech_audio = AudioSegment.silent(duration=0)

        for segment in speech_timestamps:
            start_ms = int(segment['start'] * 1000)
            end_ms = int(segment['end'] * 1000)
            speech_audio += audio[start_ms:end_ms]

        out_path = wav_path.replace(".wav", "_vad.wav")
        speech_audio.export(out_path, format="wav")
        return out_path

    def concatenate_wavs(self, wav_files: List[str], output_path: str) -> str:
        """
        Склеивает список WAV файлов в один (16kHz, 1 канал)
        """
        celery_logger.info(f"Склейка {len(wav_files)} файлов в {output_path}")

        list_file = os.path.join(self.tmp_root, f"{uuid.uuid4().hex}_list.txt")
        with open(list_file, "w") as f:
            for wav in wav_files:
                f.write(f"file '{wav}'\n")

        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            output_path
        ], check=True)

        return output_path

    def process_large_file_with_vad(self, input_path: str, chunk_length: int = 60) -> str:
        """
 +       Обработка большого файла: разбиение, конвертация, VAD, склейка.
        """
        celery_logger.info(f"Обработка большого файла: {input_path}")
        chunks = self.split_audio(input_path, chunk_length)
        vad_wavs = []

        for chunk in chunks:
            base = os.path.splitext(chunk)[0]
            wav_path = self.convert_to_wav(chunk, base + ".wav")
            vad_path = self.apply_vad(wav_path)
            vad_wavs.append(vad_path)

        final_output = os.path.splitext(input_path)[0] + f"_{uuid.uuid4().hex}_final.wav"
        return self.concatenate_wavs(vad_wavs, final_output)
