FROM python:3.10-slim-buster

WORKDIR /workdir

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . /workdir

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PORT=5000

EXPOSE $PORT

HEALTHCHECK CMD curl --fail http://localhost:5000/_stcore/health

ENTRYPOINT [ "streamlit", "run" , "dalle/app.py", "--server.port", $PORT, "--server.address=0.0.0.0"]