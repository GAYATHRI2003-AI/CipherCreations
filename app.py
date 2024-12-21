import streamlit as st
import string
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK data if not already done
nltk.download('punkt')
nltk.download('stopwords')

# Pricing model
PRICE_PER_TOKEN = 0.50  # Price per token in dollars (updated to $0.50)

def scrape_website(url):
    """
    Scrapes text content from the given website URL.
    
    Args:
        url (str): The website URL to scrape.
        
    Returns:
        str: Extracted text content from the website.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the website content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from the webpage
        text = soup.get_text(separator=' ')
        return text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the website: {e}")
        return ""

def tokenize_and_calculate(text):
    """
    Tokenizes input text, removes stop words and punctuations, and calculates token count.
    
    Args:
        text (str): The input text to process.
        
    Returns:
        dict: Contains original tokens, cleaned tokens, token count, and pricing.
    """
    # Define stop words and punctuation set
    stop_words = set(stopwords.words('english'))
    punctuations = set(string.punctuation)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stop words and punctuations
    cleaned_tokens = [word for word in tokens if word.lower() not in stop_words and word not in punctuations]
    
    # Calculate pricing based on the cleaned tokens
    total_price = len(cleaned_tokens) * PRICE_PER_TOKEN
    
    # Return the result
    return {
        "original_tokens": tokens,
        "cleaned_tokens": cleaned_tokens,
        "token_count": len(cleaned_tokens),
        "total_price": total_price
    }

# Streamlit Front-End
def display_app():
    # AI-Themed background
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://path-to-your-ai-themed-background.jpg');
            background-size: cover;
            background-position: center;
            color: white;
        }
        .stButton>button {
            background-color: #2a5d8f;
            color: white;
            border-radius: 8px;
            font-weight: bold;
        }
        .stTextInput>div>input {
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
            border: 2px solid #2a5d8f;
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Title of the app
    st.title("AI-Text Processor")

    # Prompt for user input
    st.subheader("Welcome to the AI Text Processor!")
    input_choice = st.radio("Choose input method:", ("Manual text input", "Provide website URL"))

    if input_choice == 'Manual text input':
        # Manual text input
        manual_text = st.text_area("Enter your text:", height=200)
        if manual_text:
            st.text("Processing your text...\n")
            result = tokenize_and_calculate(manual_text)
    
    elif input_choice == 'Provide website URL':
        # Website URL input
        url = st.text_input("Enter the website URL:")
        if url:
            st.text("Fetching content from the website...\n")
            # Scrape text content from the website
            scraped_text = scrape_website(url)
            
            if scraped_text:
                st.success("Website content fetched successfully!\n")
                result = tokenize_and_calculate(scraped_text)
            else:
                st.error("Failed to fetch or process the website content.")
                return
    
    # Display results
    if 'result' in locals():
        st.subheader("Results")

        # Display original and cleaned tokens
        st.write("Original Tokens (First 50):")
        st.write(result["original_tokens"][:50])

        st.write("\nCleaned Tokens (First 50):")
        st.write(result["cleaned_tokens"][:50])

        st.write("\nToken Count (Excluding Stop Words and Punctuations):")
        st.write(result["token_count"])

        st.write("\nTotal Price for Cleaned Tokens ($0.50 per token):")
        st.write(f"${result['total_price']:.2f}")

# Main function to run the app
if __name__ == '__main__':
    display_app()
