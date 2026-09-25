from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class SentimentRequest(BaseModel):
    sentences: list[str]


positive_words = {
    "love", "like", "great", "good", "excellent", "amazing",
    "awesome", "happy", "wonderful", "fantastic", "best",
    "enjoy", "enjoyed", "perfect", "nice", "beautiful",
    "success", "successful", "thank", "thanks", "glad"
}

negative_words = {
    "hate", "terrible", "bad", "awful", "sad", "horrible",
    "worst", "poor", "angry", "disappointed", "disappointing",
    "fail", "failed", "failure", "problem", "wrong", "pain",
    "boring", "annoying", "useless", "dislike"
}


def get_sentiment(sentence: str) -> str:
    text = sentence.lower()

    positive_count = sum(word in text for word in positive_words)
    negative_count = sum(word in text for word in negative_words)

    if positive_count > negative_count:
        return "happy"
    elif negative_count > positive_count:
        return "sad"
    else:
        return "neutral"


@app.post("/sentiment")
def sentiment(request: SentimentRequest):
    results = []

    for sentence in request.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": get_sentiment(sentence)
        })

    return {"results": results}
