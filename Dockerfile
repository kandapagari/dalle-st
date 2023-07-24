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
RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install --no-dev

ENV PORT=5000

EXPOSE 5000

ENTRYPOINT [ "python", "dalle/app.py"]
