# Base stage for dependency installation
FROM python:3.11-slim-bullseye AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements file to leverage Docker caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM base AS final

# Copy application code
COPY . /app/

# Create a non-root user
RUN useradd --create-home appuser
USER appuser

# Expose the port the application listens on
EXPOSE 8000

# Add a health check for AWS ECS
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD curl --fail http://localhost:8000/healthz || exit 1

# Default command to run the application
CMD ["python", "-m", "ingestion.reddit_ingestion"]
