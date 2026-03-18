FROM python:3.12-slim

# Prevents Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for Postgres
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (improves Docker caching)
COPY requirements/ /app/requirements/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/local.txt

# Copy the rest of the code
COPY . /app/

# Move to where manage.py lives
WORKDIR /app/src

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]