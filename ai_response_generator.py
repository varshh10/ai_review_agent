import os
import openai
import pandas as pd
from textblob import TextBlob
from difflib import SequenceMatcher
import faiss
import numpy as np



openai.api_key = os.getenv("OPEN_API_KEY")

# Load FAQ data (replace with your own path)
faq_df = pd.read_csv('cleaned_faq.csv')  # Make sure 'faq.csv' contains your FAQ data

# Function to get embeddings from OpenAI API
def get_embeddings(texts):
    response = openai.Embedding.create(
        input=texts,
        model="text-embedding-ada-002"  # OpenAI's embedding model for textual data
    )
    return [embedding['embedding'] for embedding in response['data']]

# Get embeddings for FAQ questions
faq_embeddings = get_embeddings(faq_df['user_query'].tolist())

# Convert embeddings to a numpy array (FAISS requires numpy arrays)
embedding_matrix = np.array(faq_embeddings).astype('float32')

# Create a FAISS index (FlatL2 is the type of index used for searching by Euclidean distance)
index = faiss.IndexFlatL2(embedding_matrix.shape[1])  # L2 distance

# Add embeddings to the index
index.add(embedding_matrix)

# Function to get review embedding
def get_review_embedding(review):
    response = openai.Embedding.create(
        input=[review],
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# Function to get the closest FAQ for a review
def get_closest_faq(review, index, faq_df):
    # Get the embedding for the user review
    review_embedding = get_review_embedding(review)
    review_embedding = np.array(review_embedding).astype('float32')

    # Search the FAISS index for the closest FAQ match
    _, I = index.search(np.array([review_embedding]), k=1)  # k=1 for closest match

    # Get the matched FAQ's product, user query, and response
    matched_faq = faq_df.iloc[I[0][0]]
    return matched_faq['user_query'], matched_faq['product_response']

# Helper function to get the best matching FAQ
def get_best_match_faq(review_text, faq_df, threshold=0.5):
    review_text = review_text.lower()
    best_match = None
    best_ratio = 0

    for idx, row in faq_df.iterrows():
        query = str(row['user_query']).lower()
        ratio = SequenceMatcher(None, review_text, query).ratio()

        if ratio > best_ratio and ratio >= threshold:
            best_ratio = ratio
            best_match = row

    return best_match

# Define the function to generate AI response
from textblob import TextBlob

def generate_ai_response(review_text, star_rating, faq_df):
    # Sentiment Analysis Logic
    if not star_rating:
        sentiment_score = TextBlob(review_text).sentiment.polarity
        if sentiment_score > 0.1:
            sentiment = "positive"
        elif sentiment_score < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
    else:
        star_rating = int(star_rating)
        if star_rating >= 4:
            sentiment = "positive"
        elif star_rating == 3:
            sentiment = "neutral"
        else:
            sentiment = "negative"

    # Response based on sentiment
    if sentiment == "positive":
        response = "Thank you for your feedback! Please do check out other features and products of Zaggle! 😊"
    elif sentiment == "neutral":
        response = "Thanks for your feedback! We're continuously working to improve. Let us know how we can enhance your experience further! 😊"
    else:
        # Handle specific negative reviews with keywords
        if "bad app" in review_text.lower() or "terrible app" in review_text.lower():
            response = "We're sorry to hear that you're having a bad experience with the app. Please let us know more details so we can improve it!"
        else:
            # Try to match the review text with FAQ
            best_match = get_best_match_faq(review_text, faq_df)
            if best_match is not None:
                response = f"Here's some information that might help:\n\n{best_match['product_response']}"
            else:
                response = "Thank you for your feedback! We're sorry to hear about the issue and are actively working on improvements. 😊"

    return response





# Main function to run the code
if __name__ == "__main__":
    review_text = input("✍️ Enter the app review: ")
    star_rating = input("⭐ Enter the star rating (1-5): ")

    # Generate response
    response = generate_ai_response(review_text, star_rating, faq_df=faq_df)
    
    print("AI Response:", response)
