FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        python3-pip \
        python3-dev \
        libglib2.0-0 \
        ffmpeg


# Copy requirements files
COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

WORKDIR .

COPY . .

ENTRYPOINT ["/usr/local/bin/gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "app:app", "-n"]