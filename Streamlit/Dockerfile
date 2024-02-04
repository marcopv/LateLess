# DockerFile
FROM python:3.8-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "info_page.py"]
