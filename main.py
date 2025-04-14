import os
import pandas as pd
from ai_response_generator import generate_ai_response
from process_reviews import process_reviews
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
def main():
    try:
        # Load and preprocess reviews
        df = process_reviews('data/appstore_reviews.csv', source='app_store')

        # ✅ Debug: Check type
        print(f"✅ Type of returned object: {type(df)}")

        if df is None or df.empty:
            print("❌ Failed to load reviews or dataframe is empty.")
            return

        # Drop rows with missing review text or star rating
        df_filtered = df.dropna(subset=["review_text", "star_rating"])

        # Keep only necessary columns
        reviews_df = df_filtered[["star_rating", "review_text", "reviewer_name"]]

        # Load FAQ data
        faq_df = pd.read_csv("cleaned_faq.csv")  # Make sure this path is correct

        print(f"🔍 Processing {len(reviews_df)} reviews...\n")

        for idx, row in reviews_df.iterrows():
            review_text = row['review_text']
            star_rating = row['star_rating']

            print(f"\n📩 Review #{idx+1}: {review_text[:100]}...")
            response = generate_ai_response(review_text, star_rating, faq_df=faq_df)  # Pass faq_df here
            print(f"🤖 AI Response: {response}")

    except FileNotFoundError:
        print("❌ 'appstore_reviews.csv' or 'cleaned_faq.csv' not found. Please check the file paths.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
