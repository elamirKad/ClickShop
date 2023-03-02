# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /usr/src/product
WORKDIR /usr/src/app

# Add requirements.txt to working directory
ADD requirements.txt /usr/src/app

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1

# Install psycopg dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .
