# Use an official lightweight Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies required by some packages (PyMuPDF, OpenSearch, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libmagic1 \
    libglib2.0-0 \
    libxrender1 \
    libxext6 \
    libsm6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --upgrade pip

# Copy requirements separately to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies (with wheels to avoid source builds)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]