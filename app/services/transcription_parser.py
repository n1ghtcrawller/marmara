import json
from typing import Optional, Any


def parse_transcription_text(text: Optional[str]) -> Optional[dict[str, Any]]:
    if not text:
        return None

    if isinstance(text, dict):
        return text

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

def get_value_from_json(text: Optional[str], key: str, default: Any = None) -> Any:
    parsed = parse_transcription_text(text)
    if isinstance(parsed, dict):
        return parsed.get(key, default)
    return default
