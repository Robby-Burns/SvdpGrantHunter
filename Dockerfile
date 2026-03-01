# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for psycopg2 (Postgres adapter)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in pyproject.toml
# We use --no-cache-dir to keep the image small
RUN pip install --no-cache-dir .

# Expose the port that Streamlit runs on
EXPOSE 8080

# Environment variables for Streamlit
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV PYTHONUNBUFFERED=1

# Initialize DB schema then run the application on the dynamic port (fallback to 8080 locally)
CMD ["sh", "-c", "python initialize_db.py && streamlit run app.py --server.port=${PORT:-8080}"]
