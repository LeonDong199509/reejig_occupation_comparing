# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install MySQL client tools and system dependencies
RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x entrypoint.sh
RUN pip install --no-cache-dir -r requirements/prod.txt

CMD ["sh", "./entrypoint.sh"]