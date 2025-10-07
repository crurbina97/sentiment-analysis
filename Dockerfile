FROM python:3.13.5-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

# ===========================
# OPTION B: Pre-download model
# ===========================
# This step downloads the model into /model_cache at build time
RUN pip3 install -r requirements.txt && \
    python3 -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    AutoModelForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english', cache_dir='/model_cache'); \
    AutoTokenizer.from_pretrained('siebert/sentiment-roberta-large-english', cache_dir='/model_cache')"
# ===========================

COPY src/ ./src/

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]