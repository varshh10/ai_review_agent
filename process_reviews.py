import pandas as pd

def process_app_store(file_path: str) -> pd.DataFrame:
    """
    Processes Apple App Store reviews CSV into a common format.
    Expected columns: 'rating', 'title', 'body', 'reviewerNickname'
    """
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    df.columns = df.columns.str.strip()  # Strip any leading/trailing spaces from column names
    
    # Debug prints to check column names
    required_cols = ['rating', 'title', 'body', 'reviewerNickname']
    print(f"Required columns: {required_cols}")
    print(f"CSV columns: {df.columns.tolist()}")
    
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Missing columns in App Store file. Required: {required_cols}")
    
    # Rename columns as needed to match the expected names in the rest of your code
    df = df.rename(columns={
        'rating': 'star_rating',  # Rename 'rating' to 'star_rating'
        'title': 'review_title',  # Rename 'title' to 'review_title'
        'body': 'review_text',    # Rename 'body' to 'review_text'
        'reviewerNickname': 'reviewer_name'  # Rename 'reviewerNickname' to 'reviewer_name'
    })

    # Keep only the necessary columns and drop rows with missing values
    df = df[['star_rating', 'review_title', 'review_text', 'reviewer_name']]
    df = df.dropna(subset=['star_rating', 'review_text', 'reviewer_name'])

    return df


import pandas as pd

def process_reviews(filepath, source='app_store'):
    try:
        df = pd.read_csv(filepath)

        # ✅ Strip whitespace from all column names
        df.columns = df.columns.str.strip()

        if source == 'app_store':
            required_cols = ['rating', 'title', 'body', 'reviewerNickname']
            if not all(col in df.columns for col in required_cols):
                print("Required columns:", required_cols)
                print("CSV columns:", list(df.columns))
                return pd.DataFrame()

            # ✅ Rename columns to standardized names
            df = df.rename(columns={
                'rating': 'star_rating',
                'body': 'review_text',
                'reviewerNickname': 'reviewer_name'
            })

        return df

    except Exception as e:
        print(f"❌ Error in process_reviews: {e}")
        return pd.DataFrame()



def add_user_review(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a user-provided review to the DataFrame.
    """
    rating = input("Enter the rating (1-5): ")
    title = input("Enter the review title: ")
    review_text = input("Enter the review text: ")
    reviewer_name = input("Enter your name: ")

    # Create a new row with the user's review
    new_review = pd.DataFrame([{
        'star_rating': rating,
        'review_title': title,
        'review_text': review_text,
        'reviewer_name': reviewer_name
    }])

    # Append the user's review to the existing DataFrame
    df = pd.concat([df, new_review], ignore_index=True)
    return df
