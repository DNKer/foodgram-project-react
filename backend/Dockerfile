FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . ./

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
