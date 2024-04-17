FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
EXPOSE 5432

ENV PYTHONUNBUFFERED=1

CMD ["/usr/local/bin/python", "-m", "src.main"]