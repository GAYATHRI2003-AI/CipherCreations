import string
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import streamlit as st

# Download NLTK data if not already done
nltk.download('punkt')
nltk.download('stopwords')

# Pricing model
PRICE_PER_TOKEN = 0.50  # Price per token in dollars

# Streamlit Configuration for Page
st.set_page_config(page_title="AI Tokenizer", layout="wide", page_icon="🤖")

# Add AI-themed style with animations (CSS)
st.markdown(
    """
    <style>
    body {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
        color: white;
    }
    .main-title {
        font-size: 3rem;
        color: #FFF;
        text-align: center;
        font-weight: bold;
        animation: fadeIn 2s ease-out;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        animation: slideIn 1s ease-out;
    }
    .sidebar .sidebar-content {
        background-color: #F0F2F6;
    }
    .results-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: fadeIn 2s ease-out;
    }
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideIn {
        from { transform: translateX(-50%); }
        to { transform: translateX(0); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title Section
st.markdown('<h1 class="main-title">AI-Powered Text Tokenizer 🤖</h1>', unsafe_allow_html=True)

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

# Sidebar UI
st.sidebar.title("Choose Input Method")
input_choice = st.sidebar.radio("Choose input method", ("Manual Text Input", "Website URL"))

# Main Section
if input_choice == "Manual Text Input":
    manual_text = st.text_area("Enter your text here:", height=300)
    if st.button("Process Text"):
        if manual_text.strip():
            result = tokenize_and_calculate(manual_text)
            st.subheader("Results")
            with st.container():
                st.markdown('<div class="results-card">', unsafe_allow_html=True)
                st.write("*Original Tokens (First 50):*")
                st.write(result["original_tokens"][:50])

                st.write("*Cleaned Tokens (First 50):*")
                st.write(result["cleaned_tokens"][:50])

                st.write("*Token Count (Excluding Stop Words and Punctuations):*")
                st.write(result["token_count"])

                st.write("*Total Price for Cleaned Tokens ($0.50 per token):*")
                st.write(f"${result['total_price']:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Please enter some text.")

elif input_choice == "Website URL":
    url = st.text_input("Enter the website URL:")
    if st.button("Fetch and Process URL"):
        if url.strip():
            st.write("Fetching content from the website...")
            scraped_text = scrape_website(url)
            if scraped_text:
                result = tokenize_and_calculate(scraped_text)
                st.subheader("Results")
                with st.container():
                    st.markdown('<div class="results-card">', unsafe_allow_html=True)
                    st.write("*Original Tokens (First 50):*")
                    st.write(result["original_tokens"][:50])

                    st.write("*Cleaned Tokens (First 50):*")
                    st.write(result["cleaned_tokens"][:50])

                    st.write("*Token Count (Excluding Stop Words and Punctuations):*")
                    st.write(result["token_count"])

                    st.write("*Total Price for Cleaned Tokens ($0.50 per token):*")
                    st.write(f"${result['total_price']:.2f}")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Failed to fetch or process the website content.")
        else:
            st.error("Please enter a valid website URL.")
