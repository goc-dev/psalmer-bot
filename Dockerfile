# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Git (needed for cloning)
RUN apt-get update && \
    apt-get install -y git

# Clone your repository with submodules
RUN git clone --recursive https://github.com/goc-dev/psalmer-bot.git /app

# Install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project files
COPY . .

# Set environment variables if needed
ENV PYTHONPATH=/app/psalmer
ENV HYMNAL_HOME_DIR=/app/hymnal-lib-external
ENV HYMNAL_MDV2_DIR=/app/hymnal-lib-external/mdv2

# Specify the command to run your bot
CMD ["python", "bots/telegram/psalmer-bot.py"]
