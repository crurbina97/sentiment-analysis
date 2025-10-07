import streamlit as st 
import pandas as pd 
from utils import load_model, analyze_sentiment, display_single_result 

# Set page configuration 
st.set_page_config( 
    page_title="Sentiment Analysis", 
    page_icon="💬", 
    layout="centered" 
) 
 
def main(): 
    st.title("💬 Sentiment Analysis with Transformers") 
    st.markdown("Enter text below to analyze sentiment using a state-of-the-art model")
    
   # Load the best model only 
    model_name = "siebert/sentiment-roberta-large-english" 
    cache_dir = "model_cache"  # Added for Cache Preload
     
    # Initialize model with loading message 
    with st.spinner("Loading model... This may take a moment on first run."): 
        classifier = load_model(model_name, cache_dir=cache_dir)
     
    if classifier is None: 
        st.error("Failed to load sentiment analysis model. Please refresh the page.") 
        return 

   # Text input area 
    text_input = st.text_area( 
        label="Enter your text:", 
        placeholder="Type or paste your text here... (e.g., 'I love this new product! It works perfectly.')", 
        height=150, 
        max_chars=1000 
    ) 
     
    # Analyze button 
    if st.button("Analyze Sentiment", type="primary", use_container_width=True): 
        if text_input.strip(): 
            with st.spinner("Analyzing sentiment..."): 
                results = analyze_sentiment(text_input, classifier) 
             
            if results: 
                display_single_result(results, text_input) 
        else: 
            st.warning("⚠️ Please enter some text to analyze.") 
 
if __name__ == "__main__": 
    main() 
