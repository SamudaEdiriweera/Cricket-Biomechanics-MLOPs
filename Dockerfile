# Use official Python lightweight image
FROM python:3.9-slim

# --- FIX: Use 'libgl1' instead of 'libgl1-mesa-glx' ---
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
# -------------------------------------------------------

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8001"]