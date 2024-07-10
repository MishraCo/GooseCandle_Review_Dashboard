# Usa una imagen de Python como base
FROM python:3.11-slim
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV OUTPUT_DIR=/app/data
# Correct setting without spaces around the equals sign
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/luminous-figure-419717-17cf4bd05e09.json

CMD ["scrapy", "crawl", "goosescrape"]