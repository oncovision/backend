# app/Dockerfile

FROM python:3.8.16

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/streamlit/streamlit-example.git.

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "survival_app_integratedview.py", "--server.enableXsrfProtection=false", "--server.port=8501", "--server.address=0.0.0.0"]
