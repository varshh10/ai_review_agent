import pickle
import numpy as np
import faiss
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
print("🔐 OPEN_API_KEY:", os.getenv("OPEN_API_KEY"))
api_key = os.getenv("OPEN_API_KEY")
print("✅ API KEY PRESENT:", api_key is not None)

client = OpenAI(api_key=api_key)

client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

# Load FAISS index and responses
with open("data/faq_index.pkl", "rb") as f:
    index, responses = pickle.load(f)

def get_faq_response(user_review: str) -> str:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=[user_review]
    )
    user_vector = np.array(response.data[0].embedding).astype("float32").reshape(1, -1)

    D, I = index.search(user_vector, k=1)
    top_index = I[0][0]

    faq_response = responses[top_index]
    
    # If there's no valid response, return a default message
    if not faq_response.strip():
        return "Sorry, we couldn't find a relevant FAQ. Please contact support."
    return faq_response

