FROM nvidia/cuda:11.6.1-devel-ubuntu20.04

WORKDIR /app

# Install Python and pip
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variable
ENV CMAKE_ARGS="-DLLAMA_CUBLAS=ON"

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --upgrade pip

# Install requirements
COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY main.py /app

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8007"]