# Use a Python base image with system dependencies for Manim
FROM python:3.13-slim-bookworm

# Set environment variables for Manim and Streamlit
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8080 \
    PORT=8080

# Install system dependencies for Manim, INCLUDING build-essential
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    libpango1.0-dev \
    ffmpeg \
    libgl1-mesa-glx \
    build-essential \  # <-- ADD THIS LINE
pkg-config \       # <-- ADD THIS LINE (often needed with build-essential for C libs)
# Other potential Manim dependencies (uncomment if you encounter issues)
# libfreetype6-dev \
# libjpeg-dev \
# zlib1g-dev \
# libsndfile1-dev \
# git \
&& rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy your requirements.txt into the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire application code into the container
COPY . .

# Expose the port Streamlit will listen on
EXPOSE 8080

# Define the command to run your Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]