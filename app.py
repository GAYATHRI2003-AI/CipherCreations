import streamlit as st
import requests
from bs4 import BeautifulSoup
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK data if not already done
nltk.download('punkt')
nltk.download('stopwords')

# Pricing model
PRICE_PER_TOKEN = 0.50  # Price per token in dollars (updated to $0.50)

# Function to scrape website content
def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=' ')
        return text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the website: {e}")
        return ""

# Function to tokenize text and calculate token count and price
def tokenize_and_calculate(text):
    stop_words = set(stopwords.words('english'))
    punctuations = set(string.punctuation)
    tokens = word_tokenize(text)
    cleaned_tokens = [word for word in tokens if word.lower() not in stop_words and word not in punctuations]
    total_price = len(cleaned_tokens) * PRICE_PER_TOKEN
    return {
        "original_tokens": tokens,
        "cleaned_tokens": cleaned_tokens,
        "token_count": len(cleaned_tokens),
        "total_price": total_price
    }

# Main function for Streamlit UI
def main():
    # Set the page layout and theme
    st.set_page_config(page_title="AI Text Scraper & Tokenizer", page_icon="🤖", layout="wide")
    
    # Add a background image to the app
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://www.example.com/ai-themed-background.jpg'); 
            background-size: cover;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Add a header with some animation
    st.title("Welcome to AI Text Scraper & Tokenizer 🤖")
    st.markdown(
        """
        <div style="color:white; font-size: 24px; text-align:center;">
        Automatically tokenize and calculate the price for your text!
        </div>
        """, unsafe_allow_html=True)

    # Provide user options for input
    input_choice = st.radio("Choose how to input text:", ('Manual Text Input', 'Provide Website URL'))

    if input_choice == 'Manual Text Input':
        user_input = st.text_area("Enter your text here:")
        if st.button("Process Text"):
            if user_input:
                result = tokenize_and_calculate(user_input)
                display_results(result)
            else:
                st.error("Please enter some text.")

    elif input_choice == 'Provide Website URL':
        url_input = st.text_input("Enter the website URL:")
        if st.button("Fetch & Process Website"):
            if url_input:
                scraped_text = scrape_website(url_input)
                if scraped_text:
                    result = tokenize_and_calculate(scraped_text)
                    display_results(result)
            else:
                st.error("Please enter a valid URL.")

# Function to display results in a formatted way
def display_results(result):
    st.subheader("Results:")
    
    st.write("### Original Tokens (First 50):")
    st.write(result["original_tokens"][:50])
    
    st.write("### Cleaned Tokens (First 50):")
    st.write(result["cleaned_tokens"][:50])
    
    st.write("### Token Count (Excluding Stop Words and Punctuations):")
    st.write(result["token_count"])
    
    st.write("### Total Price for Cleaned Tokens ($0.50 per token):")
    st.write(f"${result['total_price']:.2f}")

if __name__ == '__main__':
    main()
