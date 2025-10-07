from transformers import pipeline
import streamlit as st
import pandas as pd
 
@st.cache_resource 
def load_model(model_name, cache_dir=None):
    """Load and cache the sentiment analysis model.""" 
    try: 
        return pipeline("sentiment-analysis", model=model_name,  return_all_scores=True)
    except Exception as e: 
        st.error(f"Error loading model {model_name}: {str(e)}") 
        return None

def analyze_sentiment(text, classifier): 
    """Analyze sentiment of the given text.""" 
    if not text.strip(): 
        return None 
    try: 
        result = classifier(text) 
        return result[0] 
    except Exception as e: 
        st.error(f"Error analyzing sentiment: {str(e)}") 
        return None 

def get_sentiment_emoji(label): 
    """Map sentiment labels to emojis.""" 
    emoji_map = { 
        'POSITIVE': '😊', 
        'NEGATIVE': '😞', 
        'NEUTRAL': '😐', 
    } 
    return emoji_map.get(label.upper(), '🤔') 

def display_single_result(results, text_input=None, model_name=None): 
    """Display sentiment analysis results with metrics, table, and chart.""" 
    if not results: 
        return 
     
    st.subheader("Analysis Results") 
     
    # Get the sentiment with highest confidence 
    best_result = max(results, key=lambda x: x['score']) 
     
    # Display metrics 
    col1, col2 = st.columns(2) 
    with col1: 
        st.metric( 
            "Predicted Sentiment", 
            f"{get_sentiment_emoji(best_result['label'])} {best_result['label']}", 
            f"{best_result['score']:.2%}" 
        ) 
     
    with col2: 
        st.metric("Confidence Score", f"{best_result['score']:.2%}") 
     
    # Display all scores in a table 
    st.subheader("Detailed Scores") 
    df = pd.DataFrame(results) 
    df['score'] = df['score'].apply(lambda x: f"{x:.2%}") 
    df['emoji'] = df['label'].apply(get_sentiment_emoji) 
    df = df[['emoji', 'label', 'score']] 
    df.columns = ['', 'Sentiment', 'Confidence'] 
     
    st.dataframe(df, use_container_width=True, hide_index=True) 

    # Display model info 
    with st.expander("ℹ️ Model Information"): 
        st.write(f"**Model:** {model_name}") 
        st.write("This model is fine-tuned on 15 datasets and achieves state-of-the-art performance.") 
        st.write("It classifies text as either POSITIVE or NEGATIVE sentiment.") 
 
def main(): 
    # Set page configuration 
    st.set_page_config( 
        page_title="Sentiment Analysis", 
        page_icon="💬", 
        layout="centered" 
    ) 
    st.title("💬 Sentiment Analysis with Transformers") 
    st.markdown("Enter text below to analyze sentiment using a state-of-the-art model")
    
    # For Twitter analysis 
    #model_name = "cardiffnlp/twitter-roberta-base-sentiment" 
    
    # For multilingual support 
    #model_name = "nlptown/bert-base-multilingual-uncased-sentiment" 
    
    # For fast performance 
    #model_name = "distilbert-base-uncased-finetuned-sst-2-english" 
    
    # Load the best model only 
    model_name = "siebert/sentiment-roberta-large-english"
    
    cache_dir = "/app/model_cache"  # Added for Cache Preload
     
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
                display_single_result(results, text_input, model_name) 
        else: 
            st.warning("⚠️ Please enter some text to analyze.") 
 
if __name__ == "__main__": 
    main() 