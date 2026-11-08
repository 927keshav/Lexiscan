# 4_devops/Dockerfile
# Build context must be the project root: docker build -f 4_devops/Dockerfile .

FROM python:3.10-slim

# Install system dependencies (Tesseract OCR + poppler for PDF rendering)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        libtesseract-dev \
        poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy entire project
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Train the NER model during build (so it's ready at runtime)
RUN python 3_nlp_engine/train_ner.py

# Expose API port
EXPOSE 5000

# Run the API
CMD ["python", "2_backend/app.py"]
