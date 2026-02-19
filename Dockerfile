# Use official Python runtime as base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Create directories for reports and screenshots
RUN mkdir -p /app/reports /app/screenshots

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    BASE_URL=https://www.saucedemo.com \
    BROWSER=chrome \
    HEADLESS=true

# Run tests
CMD ["pytest", "tests/", "-v", "--html=reports/report.html", "--self-contained-html"]
