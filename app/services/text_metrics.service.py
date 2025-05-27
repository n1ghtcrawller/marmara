import re
from collections import Counter
import nltk
import pymorphy2
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

class TextMetricService:
    def __init__(self, lang="russian"):
        self.morph = pymorphy2.MorphAnalyzer()
        self.stop_words = set(stopwords.words(lang))

    def analyze(self, text: str) -> dict:
        words = nltk.word_tokenize(text.lower())
        words = [w for w in words if re.match(r'\w+', w)]
        total_words = len(words)
        unique_words = set(words)

        avg_word_length = sum(len(w) for w in words) / total_words if total_words > 0 else 0
        stopword_count = sum(1 for w in words if w in self.stop_words)

        pos_counts = Counter()
        for word in words:
            parsed = self.morph.parse(word)
            if parsed:
                tag = parsed[0].tag.POS  # существительное, глагол и т.д.
                if tag:
                    pos_counts[tag] += 1

        return {
            "word_count": total_words,
            "unique_word_count": len(unique_words),
            "avg_word_length": round(avg_word_length, 2),
            "stopword_count": stopword_count,
            "noun_count": pos_counts.get("NOUN", 0),
            "verb_count": pos_counts.get("VERB", 0),
            "adj_count": pos_counts.get("ADJF", 0),
        }
