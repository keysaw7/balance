FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système pour PyTorch
RUN apt-get update && apt-get install -y     build-essential     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "-m", "zeus.main", "--host", "0.0.0.0", "--port", "8001"]
