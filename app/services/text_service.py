import spacy
import nltk
from pymorphy2 import MorphAnalyzer
from app.logger import celery_logger

class TextService:
    def __init__(self):
        celery_logger.info("Инициализация TextService")
        nltk.download("punkt")
        self.nlp = spacy.load("ru_core_news_sm")
        self.morph = MorphAnalyzer()
        celery_logger.info("TextService инициализирован")

    def analyze(self, text: str):
        celery_logger.info("Начат анализ текста")
        doc = self.nlp(text)
        lemmas = [token.lemma_ for token in doc if not token.is_punct]
        morphs = [self.morph.parse(word)[0].tag for word in text.split()]
        result = {"lemmas": lemmas, "morphs": list(map(str, morphs))}
        celery_logger.info(f"Анализ завершён: {result}")
        return result