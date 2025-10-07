FROM python:3.13.5-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

COPY src/ ./src/

#############################
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user\
	PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app
RUN pip install --no-cache-dir --upgrade pip
COPY --chown=user . $HOME/app
#############################

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
