FROM python:3.10-slim

WORKDIR /app

COPY backend/src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src/ .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]