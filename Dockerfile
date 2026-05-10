FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything including results.json
COPY . .

# Make sure dashboard folder exists
RUN mkdir -p dashboard

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "dashboard/app.py"]