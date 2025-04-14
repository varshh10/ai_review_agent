from openai import OpenAI
import pandas as pd
import numpy as np
import os
import pickle
from dotenv import load_dotenv

import faiss

# Load environment variables (make sure OPENAI_API_KEY is set in your .env file)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

# Load FAQ data
faq_df = pd.read_csv("data/cleaned_faq.csv")
print("Column names:", faq_df.columns.tolist())  # ← Add this


# Get user queries
#faq_df["product_response"] = faq_df["product_response"].fillna("").astype(str)

faq_df["product_response"] = faq_df["product_response"].fillna("").astype(str)  # Add this line BEFORE filtering
faq_df = faq_df[faq_df["product_response"].str.strip() != ""]         # Now this will actually work

faq_df["product_response"] = faq_df["product_response"].str.strip()  #Remove leading/trailing spaces

faq_df["user_query"] = faq_df["user_query"].fillna("").astype(str)
queries = faq_df["user_query"].tolist()

responses = faq_df["product_response"].tolist()
print("Responsed before saving: ")
for i,r in enumerate(responses):
    print(f"{i}: {repr(r)}")


# Get embeddings using OpenAI
print("🔍 Generating embeddings...")
embeddings = []
for q in queries:
    response = client.embeddings.create(
        input=q,
        model="text-embedding-ada-002"
    )
    embeddings.append(response.data[0].embedding)

# Convert to numpy array
faq_embeddings = np.array(embeddings)

# Save embeddings and index
os.makedirs("data", exist_ok=True)
np.save("data/faq_embeddings.npy", faq_embeddings)

# Build FAISS index
index = faiss.IndexFlatL2(faq_embeddings.shape[1])
index.add(faq_embeddings)

# Save both embeddings and the full FAQ dataframe
#with open("data/faq_index.pkl", "wb") as f:
 #   pickle.dump({
 #       "embeddings": faq_embeddings,
  #      "faq_df": faq_df
   # }, f)



with open("data/faq_index.pkl", "wb") as f:
    pickle.dump((index, responses), f)



print("✅ Index and FAQ data saved to:", os.path.abspath("data/faq_index.pkl"))



