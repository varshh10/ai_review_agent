def generate_response(review: str, matched_faq: str, sentiment: str) -> str:
    if sentiment == "positive":
        return (
            "Thank you so much! 💙 We're thrilled you're enjoying the app. "
            "Here’s a feature you might like:\n\n" + matched_faq
        )
    elif sentiment == "negative":
        return (
            "We're really sorry to hear that. 🙁 Please contact our support team so we can help. "
            "Here’s some info that might assist you:\n\n" + matched_faq
        )
    else:
        return (
            "Thank you for your feedback! Here's some helpful info:\n\n" + matched_faq
        )
def get_positive_response(review: str) -> str:
    return (
        "Thank you so much! 💙 We're thrilled you're enjoying the app. "
        "If you haven't yet, check out some of our newest features — we think you'll love them!"
    )

def format_response_with_faq(faq_answer: str) -> str:
    return f"Sorry to hear that. 🙁 Here's some info that might help:\n{faq_answer}"
