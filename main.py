from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SentimentRequest(BaseModel):
    sentences: list[str]


positive_words = {
    "love", "loved", "like", "liked", "likes",
    "great", "good", "excellent", "amazing", "awesome",
    "happy", "happiness", "wonderful", "fantastic",
    "best", "enjoy", "enjoyed", "perfect", "nice",
    "beautiful", "success", "successful", "thank",
    "thanks", "glad", "excited", "exciting", "fun",
    "helpful", "positive", "win", "won", "delight",
    "delighted", "pleasant", "pleased", "brilliant",
    "superb", "outstanding", "impressive", "satisfied",
    "satisfying", "recommend", "recommended", "favorite"
}

negative_words = {
    "hate", "hated", "hates",
    "terrible", "bad", "awful", "sad", "horrible",
    "worst", "poor", "angry", "disappointed",
    "disappointing", "fail", "failed", "failure",
    "problem", "wrong", "pain", "boring", "annoying",
    "useless", "dislike", "disliked", "negative",
    "broken", "difficult", "worried", "worry", "upset",
    "unhappy", "loss", "lost", "disaster", "disgusting",
    "disgusted", "frustrating", "frustrated", "sadness",
    "regret", "regrettable", "horrible", "dreadful",
    "inferior", "disaster", "complaint", "complain",
    "complained", "refund", "delay", "delayed",
    "worse", "worst", "dislike", "fear", "scared"
}


positive_phrases = [
    "i love",
    "i really love",
    "i like",
    "really good",
    "very good",
    "so good",
    "very nice",
    "really nice",
    "very happy",
    "really happy",
    "highly recommend",
    "well done",
    "great job",
    "works perfectly",
    "love it",
    "like it",
    "looks great",
    "feels great"
]

negative_phrases = [
    "i hate",
    "i really hate",
    "i dislike",
    "really bad",
    "very bad",
    "so bad",
    "very sad",
    "really sad",
    "very terrible",
    "really terrible",
    "very disappointed",
    "really disappointed",
    "not good",
    "not great",
    "not happy",
    "does not work",
    "doesn't work",
    "did not work",
    "didn't work",
    "worst experience",
    "terrible experience",
    "very poor",
    "really poor",
    "hate it",
    "dislike it"
]


def get_sentiment(sentence: str) -> str:
    text = sentence.lower().strip()

    # Normalize punctuation
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text)

    positive_score = 0
    negative_score = 0

    # Phrase matching
    for phrase in positive_phrases:
        if phrase in text:
            positive_score += 3

    for phrase in negative_phrases:
        if phrase in text:
            negative_score += 3

    # Word matching
    words = text.split()

    for word in words:
        if word in positive_words:
            positive_score += 1

        if word in negative_words:
            negative_score += 1

    # Handle common negations
    negations = {"not", "no", "never", "neither", "hardly"}

    for i, word in enumerate(words):
        if word in negations and i + 1 < len(words):
            next_word = words[i + 1]

            if next_word in positive_words:
                positive_score -= 2
                negative_score += 2

            elif next_word in negative_words:
                negative_score -= 2
                positive_score += 2

    if positive_score > negative_score:
        return "happy"

    if negative_score > positive_score:
        return "sad"

    return "neutral"


@app.get("/")
def home():
    return {"message": "Sentiment API is running"}


@app.post("/sentiment")
def sentiment(request: SentimentRequest):
    results = []

    for sentence in request.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": get_sentiment(sentence)
        })

    return {"results": results}
