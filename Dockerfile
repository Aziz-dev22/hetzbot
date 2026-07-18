FROM python:3.11-slim

WORKDIR /app

# نصب پیشنیاز ها
RUN apt-get update && apt-get install -y curl gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# کپی requirements و نصب
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . .

# تایم زون ایران
ENV TZ=Asia/Tehran
