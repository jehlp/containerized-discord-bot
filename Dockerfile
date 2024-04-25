FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get install -y ffmpeg
RUN rm -rf /var/lib/apt/lists/* 

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/usr/local/bin/python", "-m", "src.main"]