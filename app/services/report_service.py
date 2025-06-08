import re
from typing import List, Dict
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

GREETING_KEYWORDS = ["здравствуйте", "добрый день", "привет"]
DISCOUNT_KEYWORDS = ["скидк", "акц", "предлож"]
TARIFF_KEYWORDS = ["тариф", "спецтариф", "план"]
SOURCE_KEYWORDS = ["интернет", "друз", "реклам", "знаком"]

CLIENT_QUESTION_PATTERNS = [
    r"(какие.*\?)", r"(что.*\?)", r"(как.*\?)", r"(где.*\?)", r"(почему.*\?)"
]

OBJECTION_KEYWORDS = ["дорог", "неудобно", "неинтересно", "позже", "не сейчас"]

FRIENDLY_WORDS = ["конечно", "пожалуйста", "рад помочь", "с удовольствием"]
RUDE_WORDS = ["что ты хочешь", "не знаю", "отстань", "не мешай"]


def detect_keywords(text: str, keywords: List[str]) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in keywords)


def extract_questions(text: str) -> List[str]:
    questions = re.findall(r"[^.?!]*\?", text)
    return [q.strip() for q in questions]


def extract_client_questions(text: str) -> List[str]:
    questions = extract_questions(text)
    client_questions = [
        q for q in questions if any(re.search(pat, q.lower()) for pat in CLIENT_QUESTION_PATTERNS)
    ]
    return client_questions


def extract_objections(text: str) -> List[str]:
    text = text.lower()
    return [word for word in OBJECTION_KEYWORDS if word in text]


def estimate_friendliness(text: str) -> int:
    text = text.lower()
    friendly_count = sum(word in text for word in FRIENDLY_WORDS)
    rude_count = sum(word in text for word in RUDE_WORDS)
    score = 5 + (friendly_count - rude_count) * 2
    return max(0, min(10, score))


def infer_product_interest(text: str) -> str:
    matches = re.findall(r"(тариф\s+\w+|план\s+\w+|услуга\s+\w+)", text.lower())
    return matches[0] if matches else ""

def analyze_openrouter_llm(transcription: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Ты эксперт по анализу звонков. Отвечай по пунктам и кратко."
            },
            {
                "role": "user",
                "content": f"""Проанализируй транскрипт звонка:
{transcription}
    

Сделай краткий анализ по следующим пунктам (до 3000 символов):
1. Общая суть и цель звонка.
2. Полезная информация, которую дал клиент или менеджер.
3. Краткая оценка работы менеджера (вежливость, информативность, вовлечённость).
4. Основные плюсы общения.
5. Основные минусы (если есть).
6. Рекомендации по улучшению (если необходимо).

Пиши лаконично, не повторяй текст звонка, а только выжимку смысла."""
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.7
    }

    try:
        response = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except httpx.RequestError as e:
        return f"Ошибка соединения с OpenRouter: {e}"
    except Exception as e:
        return f"Ошибка анализа ответа: {e}"

def generate_report_data(text: str) -> Dict:
    return {
        "greeting": detect_keywords(text, GREETING_KEYWORDS),
        "offered_discount": detect_keywords(text, DISCOUNT_KEYWORDS),
        "offered_special_tariff": detect_keywords(text, TARIFF_KEYWORDS),
        "client_questions": extract_client_questions(text),
        "friendliness_score": estimate_friendliness(text),
        "product_interest": infer_product_interest(text),
        "client_objections": extract_objections(text),
        "client_knows_source": detect_keywords(text, SOURCE_KEYWORDS),
    }
