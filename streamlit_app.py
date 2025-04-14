import streamlit as st
import pandas as pd
from ai_response_generator import generate_ai_response

st.set_page_config(page_title="AI Review Responder", layout="centered")

@st.cache_data
def load_faq_data():
    return pd.read_csv("cleaned_faq.csv")

faq_df = load_faq_data()

st.title("🤖 AI Review Response Generator")
st.markdown("Please enter an app review and select a star rating to generate a smart AI response.")

# Create input fields for review and star rating
col1, col2 = st.columns([3, 1])
with col1:
    review = st.text_area("✍️ Enter the app review:", height=180)
with col2:
    star_rating = st.number_input("⭐ Star Rating (1-5):", min_value=1, max_value=5, step=1)

# Button to generate response
st.markdown("---")
generate_button = st.button("Generate Response")

# Clear button
clear_button = st.button("Clear Fields")

if clear_button:
    review = ""
    star_rating = 1

if generate_button:
    if not review.strip():
        st.warning("Please enter a review before generating a response.")
    else:
        with st.spinner("Generating a smart response..."):
            response = generate_ai_response(review, star_rating, faq_df=faq_df)
        
        st.markdown("### ✅ AI-Generated Response")
        st.success(response)
