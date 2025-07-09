# Use a Python base image with system dependencies for Manim
# It's crucial to pick an image that has common build tools and can easily install Manim's dependencies.
# A Debian-based image is usually a good starting point.
FROM python:3.13-slim-bookworm

# Set environment variables for Manim and Streamlit
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8080 \
    PORT=8080

# Install system dependencies for Manim
# These include Cairo, Pango, FFMpeg, and other libraries Manim relies on.
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    libgl1-mesa-glx \
    # Other potential Manim dependencies (uncomment if you encounter issues)
    # pkg-config \
    # libfreetype6-dev \
    # libjpeg-dev \
    # zlib1g-dev \
    # libsndfile1-dev \
    # git \
    # build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy your requirements.txt into the container
COPY requirements.txt ./

# Install Python dependencies
# You might need to adjust versions in requirements.txt if they conflict with Manim's system requirements.
# Use --no-cache-dir to save space.
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire application code into the container
COPY . .

# Expose the port Streamlit will listen on
EXPOSE 8080

# Define the command to run your Streamlit application
# Cloud Run expects your service to listen on the PORT environment variable.
CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]