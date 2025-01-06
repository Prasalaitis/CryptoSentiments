# Use a specific lightweight Python base image
FROM python:3.9.15-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Add build-time argument for environment
ARG ENV=production
ENV ENV=${ENV}

# Copy only requirements first (to leverage Docker caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Create a non-root user for security
RUN useradd --create-home appuser
USER appuser

# Expose the port the application listens on
EXPOSE 8000

# Add a health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD curl --fail http://localhost:8000/healthz || exit 1

# Default command to run the application
CMD ["python", "reddit_ingestion.py"]
