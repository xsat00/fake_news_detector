from langdetect import detect
import spacy
from transformers import pipeline

# Load multilingual sentiment/emotion analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Named Entity Recognition using spaCy (multilingual)
try:
    nlp = spacy.load("xx_ent_wiki_sm")
except:
    import os
    os.system("python -m spacy download xx_ent_wiki_sm")
    nlp = spacy.load("xx_ent_wiki_sm")

def analyze_caption(caption):
    result = {
        "clickbait_words": [],
        "named_entities": [],
        "emotive_words": [],
        "flagged": False
    }

    # Language detection
    try:
        lang = detect(caption)
    except:
        lang = 'unknown'

    # Basic clickbait detection (expand list as needed)
    clickbait_terms = ["shocking", "unbelievable", "you won’t believe", "must watch", "exclusive", "breaking"]
    for word in clickbait_terms:
        if word.lower() in caption.lower():
            result["clickbait_words"].append(word)

    # Named Entity Recognition
    doc = nlp(caption)
    for ent in doc.ents:
        result["named_entities"].append([ent.text, ent.label_])

    # Sentiment/emotive analysis
    try:
        sentiment = sentiment_pipeline(caption)[0]
        score = sentiment.get("score", 0)
        label = sentiment.get("label", "")

        # Flag if highly emotive
        if "5" in label or score > 0.95:
            result["emotive_words"].append(label)
            result["flagged"] = True
    except Exception as e:
        result["emotive_words"].append("Could not analyze sentiment")

    return result
