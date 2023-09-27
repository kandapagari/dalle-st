FROM python:3.11-slim

WORKDIR /workdir

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl software-properties-common \
    git ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY . /workdir

RUN pip install --upgrade pip
RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install --no-dev

ENV PORT=5000

EXPOSE 5000

HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1

ENTRYPOINT [ "python", "dalle/app.py"]
