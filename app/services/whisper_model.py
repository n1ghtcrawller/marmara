import whisper
from threading import Lock
import torch

_model = None
_lock = Lock()

def get_whisper_model(model_name="large-v2"):
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                device = "cuda" if torch.cuda.is_available() else "cpu"
                _model = whisper.load_model(model_name, device=device)
    return _model
