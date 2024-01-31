FROM python:3.12-bookworm

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY .env /.env
COPY . /

RUN pip install -U pip && \
    pip install --no-cache-dir -e /

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "38000", "--env-file", ".env"]
