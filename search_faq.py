import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

# Load the pre-trained model (ensure it's the same one used during indexing)
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text):
    """
    Generates an embedding for the given text using a pre-trained model.

    Parameters:
    - text (str): The input text to be embedded.

    Returns:
    - numpy.ndarray: The embedding vector for the input text.
    """
    embedding = model.encode(text)
    return embedding

# Define the path to the FAISS index file
index_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../outputs/faq_index.faiss'))

# Load the index
if os.path.exists(index_file_path):
    index = faiss.read_index(index_file_path)
    print("FAISS index loaded successfully.")
else:
    raise FileNotFoundError(f"FAISS index file not found at {index_file_path}")

def search_faq(query, k=5):
    """
    Searches the FAISS index for the top k most similar FAQs to the input query.

    Parameters:
    - query (str): The user's query.
    - k (int): The number of top similar FAQs to retrieve.

    Returns:
    - List of tuples containing the indices and distances of the top k similar FAQs.
    """
    # Convert the query into a vector embedding
    # Note: Replace this with your actual embedding generation method
    query_vector = generate_embedding(query)

    # Ensure the query vector has the correct shape
    query_vector = np.array(query_vector).astype('float32').reshape(1, -1)

    # Perform the search
    distances, indices = index.search(query_vector, k)

    return list(zip(indices[0], distances[0]))

if __name__ == "__main__":
    test_query = "What is the purpose of the app?"
    results = search_faq(test_query)
    print("Search results:", results)

