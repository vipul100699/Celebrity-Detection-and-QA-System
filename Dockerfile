## Use a small, supported Python base image
FROM python:3.13-slim

## Essential environment variables
## PYTHONDONTWRITEBYTECODE: Prevent creation of .pyc files
## PYTHONUNBUFFERED: Enable unbuffered logging for real-time output
## PIP_NO_CACHE_DIR: Disable pip cache to reduce image size
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

## Work directory inside the Docker container
WORKDIR /app

## Installing system dependencies (including OpenCV dependencies)
## libgl1, libglib2.0-0, etc. are required for cv2 (OpenCV) to work properly
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
# If requirements.txt hasn't changed, this step (and the install step) will be cached
COPY requirements.txt pyproject.toml /app/

## Install python dependencies
RUN pip install -r requirements.txt

## Copying your all contents from local to app directory
COPY . /app

# Expose port 5000 for the Flask application
EXPOSE 5000

# Run the app using python
CMD ["python", "app.py"]