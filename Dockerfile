FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Make sure results.json exists
RUN mkdir -p dashboard && \
    echo '{"latest":{"file":"No submissions yet","type":"N/A","score":0,"max_score":10,"status":"N/A","timestamp":"N/A","checks":[]},"results":[]}' \
    > dashboard/results.json

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "dashboard/app.py"]