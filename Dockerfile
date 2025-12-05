## Use a small, supported Python base image
FROM python:3.13-slim

## Essential environment variables
## Prevent creation of .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

## Work directory inside the Docker container
WORKDIR /app

## Installing system dependencies (including OpenCV dependencies)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Upgrade pip early to avoid any old wheel issue
RUN python -m pip install --upgrade pip

# Copy only dependency files first to leverage docker cache
COPY requirements.txt pyproject.toml /app/

## Install dependencies
RUN pip install -r requirements.txt

## Copying your all contents from local to app
COPY . /app

# Used PORTS
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]