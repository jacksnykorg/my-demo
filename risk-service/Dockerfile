# Using a non-slim base image to trigger a Snyk IaC finding
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposing the port
EXPOSE 8000

# The container will run as root by default, another Snyk finding.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]