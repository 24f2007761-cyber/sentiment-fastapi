from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


# Allow requests from the assignment evaluator
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
    "love",
    "loved",
    "like",
    "liked",
    "great",
    "good",
    "excellent",
    "amazing",
    "awesome",
    "happy",
    "happiness",
    "wonderful",
    "fantastic",
    "best",
    "enjoy",
    "enjoyed",
    "perfect",
    "nice",
    "beautiful",
    "success",
    "successful",
    "thank",
    "thanks",
    "glad",
    "excited",
    "exciting",
    "fun",
    "helpful",
    "positive",
    "win",
    "won",
}


negative_words = {
    "hate",
    "hated",
    "terrible",
    "bad",
    "awful",
    "sad",
    "horrible",
    "worst",
    "poor",
    "angry",
    "disappointed",
    "disappointing",
    "fail",
    "failed",
    "failure",
    "problem",
    "wrong",
    "pain",
    "boring",
    "annoying",
    "useless",
    "dislike",
    "disliked",
    "negative",
    "broken",
    "hard",
    "difficult",
    "worried",
    "worry",
    "upset",
    "unhappy",
    "badly",
    "loss",
    "lost",
}


def get_sentiment(sentence: str) -> str:
    text = sentence.lower()

    positive_count = 0
    negative_count = 0

    for word in positive_words:
        if word in text:
            positive_count += 1

    for word in negative_words:
        if word in text:
            negative_count += 1

    if positive_count > negative_count:
        return "happy"

    if negative_count > positive_count:
        return "sad"

    return "neutral"


@app.get("/")
def home():
    return {"message": "Sentiment API is running"}


@app.post("/sentiment")
def sentiment(request: SentimentRequest):
    results = []

    for sentence in request.sentences:
        results.append(
            {
                "sentence": sentence,
                "sentiment": get_sentiment(sentence),
            }
        )

    return {"results": results}
