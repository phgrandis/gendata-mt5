FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.mt5.txt

CMD ["python", "main.py"]
