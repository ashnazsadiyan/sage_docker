FROM nvidia/cuda:11.4.3-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        python3-pip \
        python3-dev \
        libglib2.0-0 \
        build-essential \
        autoconf \
        automake \
        cmake \
        libass-dev \
        libfreetype6-dev \
        libsdl2-dev \
        libtool \
        libva-dev \
        libvdpau-dev \
        libvorbis-dev \
        libxcb1-dev \
        libxcb-shm0-dev \
        libxcb-xfixes0-dev \
        pkg-config \
        texinfo \
        wget \
        zlib1g-dev

# Clone FFmpeg repository
RUN git clone https://git.ffmpeg.org/ffmpeg.git

# Change directory to ffmpeg
WORKDIR /ffmpeg

# Configure FFmpeg with CUDA support
RUN ./configure --enable-cuda --enable-cuvid --enable-nvenc --enable-nonfree --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --extra-ldflags=-L/usr/local/cuda/lib64

# Compile and install FFmpeg
RUN make -j$(nproc)
RUN make install

# Continue with the rest of your Dockerfile...

# Copy requirements files
COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

WORKDIR .

COPY . .

ENTRYPOINT ["/usr/local/bin/gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "app:app", "-n"]
