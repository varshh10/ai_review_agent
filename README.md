# 🤖 AI App Review Responder

This project builds an AI-powered app review responder that intelligently handles both positive and negative reviews. It processes reviews, analyzes sentiment, and provides an empathetic response using a knowledge base of frequently asked questions (FAQs).

---

## 🌟 Features
- **Sentiment Analysis**: Determines whether a review is positive, negative, or neutral based on star rating or sentiment analysis.
- **FAQ-Based Responses**: For negative reviews, the system pulls the most relevant information from a FAQ database to provide helpful responses.
- **User-Friendly UI**: Easy-to-use interface for entering reviews and receiving responses (via terminal or web app with Streamlit).
- **Customizable**: Simple to extend and modify the FAQ knowledge base and response generation logic.

---

## 🛠️ Setup & Installation
### 1. **Clone the Repository**
```bash 
git clone https://github.com/YOUR_USERNAME/ai-review-agent.git
cd ai-review-agent
```
### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Set up OpenAI API Key
- Make sure to set your OpenAI API key in the environment.
- Create a .env file in the project root and add your key:
```bash
OPENAI_API_KEY=your_api_key_here
```
## 🖥️ Usage
### Option 1: Run the Terminal Interface
Run the script
```bash
python main.py
```
View the output in the terminal for each review.
### Option 2: Run the Web Interface with Streamlit
Start the Streamlit app:
```bash
streamlit run app.py
```
Enter a review and star rating in the UI to get a response.
