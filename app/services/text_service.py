import spacy
import nltk
from pymorphy2 import MorphAnalyzer

class TextService:
    def __init__(self):
        nltk.download("punkt")
        self.nlp = spacy.load("ru_core_news_sm")
        self.morph = MorphAnalyzer()

    def analyze(self, text: str):
        doc = self.nlp(text)
        lemmas = [token.lemma_ for token in doc if not token.is_punct]
        morphs = [self.morph.parse(word)[0].tag for word in text.split()]
        return {"lemmas": lemmas, "morphs": list(map(str, morphs))}