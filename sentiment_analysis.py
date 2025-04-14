from textblob import TextBlob

def get_sentiment(text: str) -> str:
    """
    Determines the sentiment of a text using polarity.
    Returns 'positive', 'negative', or 'neutral'.
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    else:
        return "neutral"
