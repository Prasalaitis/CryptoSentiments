# Use a lightweight Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1     # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED=1            # Ensure stdout and stderr are flushed immediately

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first (to leverage Docker caching for dependencies)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Create a non-root user for security
RUN useradd --create-home appuser
USER appuser

# Expose the port the application listens on (if applicable)
EXPOSE 8000

# Default command to run the application
CMD ["python", "reddit_ingestion.py"]
