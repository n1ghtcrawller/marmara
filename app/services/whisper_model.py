import whisper
from threading import Lock

_model = None
_lock = Lock()

def get_whisper_model(model_name="large-v2"):
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                _model = whisper.load_model(model_name, device="cuda")
    return _model
