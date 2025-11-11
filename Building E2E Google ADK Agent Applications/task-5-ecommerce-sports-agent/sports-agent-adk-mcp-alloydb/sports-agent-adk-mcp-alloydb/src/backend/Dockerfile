# src/backend/Dockerfile
FROM python:3.11-slim


WORKDIR /app

# security: non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# minimal build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
 && rm -rf /var/lib/apt/lists/*

# deps first (cache-friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# app code
COPY . .


RUN chown -R appuser:appuser /app


USER appuser



ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080





EXPOSE 8080





# use exec form; fixed port 8080 to match Cloud Run
ENTRYPOINT ["python","-m","uvicorn","app:app","--host","0.0.0.0","--port","8080"]

