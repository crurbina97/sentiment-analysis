from transformers import pipeline
import streamlit as st
import pandas as pd
 
@st.cache_resource 
def load_model(model_name, cache_dir=None):
    """Load and cache the sentiment analysis model.""" 
    try: 
        return pipeline(
            "sentiment-analysis",
            model=model_name,
            tokenizer=model_name,     # Optional but good practice
            return_all_scores=True,
            cache_dir=cache_dir       #  use the pre-downloaded folder
        )
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

[ 
    {'label': 'POSITIVE', 'score': 0.9998}, 
    {'label': 'NEGATIVE', 'score': 0.0002} 
] 

def display_single_result(results, text_input=None): 
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

# For Twitter analysis 
#model_name = "cardiffnlp/twitter-roberta-base-sentiment" 
 
# For multilingual support 
#model_name = "nlptown/bert-base-multilingual-uncased-sentiment" 
 
# For fast performance 
#model_name = "distilbert-base-uncased-finetuned-sst-2-english" 

# Load the best model only 
model_name = "siebert/sentiment-roberta-large-english" 