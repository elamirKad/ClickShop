# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV SECRET_KEY 'mo!Pgg3e&45FHkX&eKGeb42u*8i!DCAeZcZGi*#kabQWibT0hD'

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
