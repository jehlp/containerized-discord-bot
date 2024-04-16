FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "source tokens.env]
CMD ["/usr/local/bin/python", "src/main.py"]
